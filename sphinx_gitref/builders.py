from sphinx.builders import Builder
from sphinx.util import logging

logger = logging.getLogger(__name__)


class NullBuilder(Builder):
    """
    Builder which doesn't write its output
    """

    name = "null"
    format = "null"

    def init(self):
        """Initialize builder-specific settings."""
        self.output = {}

    def get_outdated_docs(self):
        """Return an iterable of input files that are outdated."""
        return "all documents"

    def get_target_uri(self, docname, typ=None):
        """Return the target URI for a document."""
        return docname

    def prepare_writing(self, docnames):
        """Prepare for writing. Not used in nofile builder."""
        pass

    def write_doc(self, docname, doctree):
        """Process a single document."""
        logger.info(f"Processing document: {docname}")
        self.output[docname] = doctree

    def finish(self):
        """Finish the building process."""
        logger.info("Finished processing all documents.")
        logger.info(f"Processed {len(self.output)} documents.")
