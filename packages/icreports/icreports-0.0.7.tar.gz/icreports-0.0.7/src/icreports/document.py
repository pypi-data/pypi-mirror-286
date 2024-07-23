import logging
import os
from pathlib import Path
import shutil

from icplot.tex_interface import TexInterface

from .link_validator import LinkValidator
from .jupyter_book_interface import JupyterBookInterface
from .config import Config
from .table_of_contents import TableOfContents

logger = logging.getLogger(__name__)


class Document:

    def __init__(self):
        pass


class Book(Document):
    def __init__(
        self,
        root: Path,
        config_path: Path | None = None,
        config: dict = {},
        version: str = "",
        toc_path: Path | None = None,
        toc: dict = {},
    ) -> None:
        super().__init__()

        self.root = root
        self.media_dir = self.root / "src/media"
        self.link_validator = LinkValidator()

        self.config = Config(config, config_path, version)
        self.toc = TableOfContents(toc, toc_path)
        if (not config) and (not config_path):
            self.config.load(root / "_config.yml")
        if (not toc_path) and (not toc):
            self.toc.load(root / "_toc.yml")

        self.tex_interface = TexInterface(None, None)
        self.build_interface = JupyterBookInterface(
            self.root, document_name=self.config.name
        )

    def validate(self):
        logger.info("Starting content validation")
        # self.link_validator.validate_links(self.pages)
        logger.info("Finished content validation")

    def set_version(self):
        logging.info("Version is: %s", self.version)

    def make_public_version(self, build_dir: Path):

        work_dir = build_dir / "public"
        if work_dir.exists():
            shutil.rmtree(work_dir)
        os.makedirs(work_dir)

        media_dir = work_dir / "src/media"
        os.makedirs(work_dir / "src")
        os.makedirs(media_dir)

        media_build_dir = build_dir / "media"
        public_media_build_dir = work_dir / "_build/media"
        os.makedirs(public_media_build_dir)

        self.config.write(work_dir / "_config.yml")

        public_toc = self.toc.get_public_version()
        public_toc.write(work_dir / "_toc.yml")

        for path in public_toc.get_file_paths():
            shutil.copy(self.root / path, work_dir / path)

        for direntry in self.media_dir.iterdir():
            if direntry.is_file():
                shutil.copy(direntry, media_dir)

        for direntry in media_build_dir.iterdir():
            if direntry.is_file():
                shutil.copy(direntry, public_media_build_dir)

        logger.info("Start generating public published output")
        self.build_interface.source_dir = work_dir
        self.build_interface.build_dir = work_dir / "_build"
        self.build_interface.build_html()
        self.build_interface.build_pdf()
        logger.info("Finished generating public published output")

        shutil.make_archive(
            str(build_dir / f"{self.config.project_name}_public"), "zip", str(work_dir)
        )

    def publish(self, build_dir: Path):

        build_dir = build_dir.resolve()

        logger.info("Loading document static content")
        self.toc.load_content(self.root)

        logger.info("Starting document checks")
        self.validate()
        logger.info("Finished document checks")

        # Generate any dynamic content, e.g. tex files
        if self.media_dir.exists():
            logger.info("Start generating dynamic content")
            self.tex_interface.build_dir = build_dir
            self.tex_interface.output_dir = build_dir / "media"
            self.tex_interface.build(self.media_dir)
            logger.info("Finish generating dynamic content")

        if self.config.split_public_version:
            logger.info("Generating public version")
            self.make_public_version(build_dir)
            logger.info("Finished generating public version")

        logger.info("Start generating published output")
        self.build_interface.source_dir = self.root
        self.build_interface.build_dir = build_dir
        self.build_interface.build_html()
        self.build_interface.build_pdf()
        logger.info("Finished generating published output")
