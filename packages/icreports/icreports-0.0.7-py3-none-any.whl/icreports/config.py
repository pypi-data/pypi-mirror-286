from pathlib import Path

import yaml

from iccore.yaml_utils import read_yaml


class Config:

    def __init__(self, data: dict = {}, path: Path | None = None, version: str = ""):
        self.data = data

        self.version: str = version
        self.project_name: str = "book"
        self.split_public_version: bool = False

        self._key: str = "icreports"

        if self.data:
            self.deserialize()
        elif path:
            self.load(path)

    def load(self, path: Path):
        self.data = read_yaml(path)
        self.deserialize()

    def deserialize(self):
        if self._key not in self.data:
            return

        if "project_name" in self.data[self._key]:
            self.name = self.data[self._key]["project_name"]

        if not self.version:
            if "version" in self.data[self._key]:
                self.version = self.data[self._key]["version"]
            else:
                self.version = "0.0.0"

        if "split_public_version" in self.data[self._key]:
            self.split_public_version = self.data[self._key]["split_public_version"]

    def serialize(self):
        ret = self.data
        if self.version:
            ret["version"] = self.version
        ret["project_name"] = self.project_name
        ret["split_public_version"] = self.split_public_version
        return ret

    def write(self, path: Path):
        with open(path, "w") as f:
            yaml.dump(self.serialize(), f)
