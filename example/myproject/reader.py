from pathlib import Path


class Reader:
    path: Path

    def __init__(self, path: Path):
        self.path = path

    def read(self):
        return self.path.read_text()


def read(file):
    file = Path(file)
    reader = Reader(file)
    content = reader.read()
    return content
