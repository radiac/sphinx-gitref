from __future__ import annotations

import ast
import hashlib
import json
from multiprocessing import Queue
from typing import TYPE_CHECKING

from sphinx.errors import SphinxError

if TYPE_CHECKING:
    from pathlib import Path
from sphinx.util.logging import getLogger

from .exceptions import ParseError
from .parser import python_to_node

logger = getLogger("sphinx_gitref")


#: Current hash file format version
FILE_VERSION = 1


def hash_text(text: str):
    print(f">>> {text}")
    hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return hash


def hash_file(path: Path):
    src = path.read_text()
    return hash_text(src)


def hash_node(node: ast.AST):
    src = ast.unparse(node)
    return hash_text(src)


class Hasher:
    #: hash file
    file: Path

    #: if we're updating the hash file, or checking it
    updating: bool

    #: List of stored hashes from the last update
    hashes: dict[str, str]

    #: Line numbers for code references
    lines: dict[str, int]

    #: Status of the hashes - checked at the start, rendered during role to make it
    #: easier to find references
    status: dict[str, bool]

    #: Target to filename and code reference (cache of self.split_target)
    name_ref: dict[str, tuple[str, str | None]]

    #: A set of targets which have been used in the docs
    used: set[str]

    #: Errors from checks
    errors: dict[str, str]

    # Queues used internally to allow parallel document processing
    hash_queue: Queue
    line_queue: Queue
    used_queue: Queue
    error_queue: Queue

    def __init__(self, file: Path, project_root: Path, updating: bool):
        self.file = file
        self.project_root = project_root
        self.updating = updating

        # Data from file
        self.hashes = {}
        self.lines = {}

        # Track checks
        self.name_ref = {}
        self.used = set()
        self.errors = {}

        self.hash_queue = Queue()
        self.line_queue = Queue()
        self.used_queue = Queue()
        self.error_queue = Queue()

        self.load()

    def load(self):
        """
        Load the hash file, if we need it and it exists
        """
        # No need to load it if we're updating, we'll ignore it anyway
        if self.updating:
            return

        # It's ok if the file doesn't exist, maybe gitref is installed but not used.
        # If it is used and the file should exist, we'll find out when checking.
        if not self.file.exists():
            logger.info(f"gitref hash file not found at {self.file}")
            self.refs = {}
            return

        refs = json.load(self.file.open())
        if refs["version"] != FILE_VERSION:
            raise ValueError(
                "Unexpected hash file version"
                f" - code understands {FILE_VERSION}, file is {refs['version']}"
            )

        self.hashes = refs["hashes"]
        self.lines = refs["lines"]

    def split_target(self, target: str) -> tuple[str, str | None]:
        """
        Convert a target into a filename and optional coderef
        """
        if "::" in target:
            filename, coderef = target.split("::", 1)
        else:
            filename = target
            coderef = None

        self.name_ref[target] = (filename, coderef)
        return filename, coderef

    def check(self):
        """
        Run a full check of the hash file against the code

        This will pre-populate a shared cache when processing in parallel
        """
        for target, hash in self.hashes.items():
            self.find_target(target, checking=True)
        self.collect_queues()

    def find_target(self, target: str, checking=False):
        """
        Find the specified target and check it against the cache, or update the cache if
        ``self.updating=True``.

        If ``checking=True`` then this will not be logged to ``self.used``
        """
        filename, coderef = self.split_target(target)
        if not checking:
            self.used_queue.put(target)

        # Ensure the file exists - can be a file or a dir
        filepath = self.project_root / filename
        if not filepath.exists():
            self.error_queue.put((target, "File not found"))
            return False

        elif coderef is None:
            hashed = hash_file(filepath)
            if self.updating:
                # Put it in both the dict for local access, and the queue for parallel
                self.hashes[target] = hashed
                self.hash_queue.put((target, hashed))
            elif target not in self.hashes:
                self.error_queue.put((target, "Unknown target"))
            elif self.hashes[target] != hashed:
                self.error_queue.put((target, "Target changed"))
            else:
                # target is in hashes and matches
                pass

        else:
            # Convert a code ref into a line number
            try:
                node = python_to_node(filepath, coderef)
            except ParseError as error:
                self.errors[target] = str(error)
                return False
            else:
                self.lines[target] = node.lineno
                hashed = hash_node(node)

                if self.updating:
                    self.hashes[target] = hashed
                    self.hash_queue.put((target, hashed))
                elif target not in self.hashes:
                    self.error_queue.put((target, "Unknown target"))
                elif self.hashes[target] != hashed:
                    self.error_queue.put((target, "Target changed"))
                else:
                    # target is in hashes and matches
                    pass

        return True

    def finish(self):
        """
        Called once all the docs have been processed
        """
        self.collect_queues()
        if self.updating:
            self.build_file()
        else:
            self.report()

    def collect_queues(self):
        for data_dict, queue in [
            (self.hashes, self.hash_queue),
            (self.lines, self.line_queue),
            (self.errors, self.error_queue),
        ]:
            while not queue.empty():
                key, value = queue.get()
                data_dict[key] = value

        for data_set, queue in [
            (self.used, self.used_queue),
        ]:
            while not queue.empty():
                data_set.add(queue.get())

    def build_file(self):
        """
        Use the found code references to build the hash file
        """
        if self.errors:
            logger.error(f"{len(self.errors)} errors building gitref:")
            logger.error(
                "\n".join(f"{target}: {error}" for target, error in self.errors.items())
            )

        self.file.touch()
        json.dump(
            {"version": FILE_VERSION, "hashes": self.hashes, "lines": self.lines},
            self.file.open("w"),
            indent=2,
        )

    def report(self):
        """
        Report on the run and raise an exception
        """

        def references(n):
            return "reference" if n == 1 else "references"

        num = len(self.used)
        logger.info(f"{num} gitref {references(num)} found")

        # Check for references we saw in the past which no longer exist
        hashes = set(self.hashes.keys())
        unused = hashes - self.used
        if unused:
            num = len(unused)
            logger.warning(
                f"gitref hash file is out of date, {num} unused {references(num)}"
            )

        extra = self.used - hashes
        if extra:
            num = len(extra)
            raise ValueError(
                f"gitref hash file is out of date, {num} missing {references(num)}"
            )

        if self.errors:
            raise SphinxError("[gitref] References failed. Build failed.")
