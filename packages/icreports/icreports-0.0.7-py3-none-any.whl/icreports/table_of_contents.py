from pathlib import Path
import yaml
import logging

from iccore.yaml_utils import read_yaml

from .part import Part
from .chapter import Section

logger = logging.getLogger(__name__)


class TableOfContents:

    def __init__(self, input: dict = {}, path: Path | None = None):
        self.format: str = "jb-book"
        self.root: Section | None = None
        self.parts: list[Part] = []

        if input:
            self.deserialize(input)
        elif path:
            self.load(path)

    def load(self, path: Path):
        self.deserialize(read_yaml(path))

    def load_content(self, root: Path):
        if self.root:
            self.root.load(root)

        for part in self.parts:
            part.load(root)

    def serialize(self):
        ret = {}
        ret["format"] = self.format
        if self.root:
            ret["root"] = str(self.root.get_path())

        if self.parts:
            ret["parts"] = []
            for part in self.parts:
                ret["parts"].append(part.serialize())
        return ret

    def get_file_paths(self) -> list[Path]:
        paths = []
        if self.root:
            paths.append(self.root.get_path_with_extension())
        for part in self.parts:
            paths.extend(part.get_file_paths())
        return paths

    def get_public_version(self):
        public_toc = TableOfContents()
        public_toc.root = self.root
        public_toc.format = self.format

        for part in self.parts:
            if part.has_public_chapters():
                public_toc.parts.append(part.get_public_version())
        return public_toc

    def deserialize(self, input: dict):

        if "format" in input:
            self.format = input["format"]

        if "root" in input:
            self.root = Section(input["root"])

        if "parts" in input:
            for entry in input["parts"]:
                part = Part()
                part.deserialize(entry)
                self.parts.append(part)

    def write(self, path: Path):
        with open(path, "w") as f:
            yaml.dump(self.serialize(), f)
