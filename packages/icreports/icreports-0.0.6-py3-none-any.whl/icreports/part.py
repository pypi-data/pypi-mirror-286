from pathlib import Path
import logging

from .chapter import Chapter

logger = logging.getLogger(__name__)


class Part:

    def __init__(self) -> None:
        self.caption: str = ""
        self.chapters: list[Chapter] = []

    def load(self, root: Path):
        for chapter in self.chapters:
            chapter.load(root)

    def get_file_paths(self) -> list[Path]:
        paths = []
        for chapter in self.chapters:
            paths.extend(chapter.get_file_paths())
        return paths

    def has_public_chapters(self):
        for chapter in self.chapters:
            if chapter.has_public_sections():
                return True
        return False

    def get_public_version(self):
        public_part = Part()
        public_part.caption = self.caption

        for chapter in self.chapters:
            if chapter.has_public_sections():
                public_part.chapters.append(chapter.get_public_version())
        return public_part

    def deserialize(self, input: dict):
        if "caption" in input:
            self.caption = input["caption"]

        if "chapters" in input:
            for entry in input["chapters"]:
                chapter = Chapter()
                chapter.deserialize(entry)
                self.chapters.append(chapter)

    def serialize(self):
        ret = {}
        if self.caption:
            ret["caption"] = self.caption

        if self.chapters:
            ret["chapters"] = []
            for chapter in self.chapters:
                ret["chapters"].append(chapter.serialize())
        return ret
