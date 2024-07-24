from argparse import Namespace
from typing import TYPE_CHECKING

from pvenv.subcommands.base import BaseCommand

if TYPE_CHECKING:
    from pathlib import Path


class Command(BaseCommand):
    def __init__(self, options: Namespace) -> None:
        super().__init__(options)
        self.base_dir: Path = options.base_dir

    def run(self) -> None:
        for directory in sorted(self.base_dir.glob("*")):
            if directory.is_dir():
                print(directory.name)
