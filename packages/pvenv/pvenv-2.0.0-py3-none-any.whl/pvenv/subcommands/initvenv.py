from argparse import Namespace
from pathlib import Path

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace) -> None:
        super().__init__(options)

    def run(self) -> None:
        print(
            "Add the following line to your shell rc:\n"
            f". {Path(__file__).parent.joinpath('scripts/pvenv.sh').absolute()}"
        )
