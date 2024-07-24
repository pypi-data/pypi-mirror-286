import os
from argparse import Namespace

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace) -> None:
        super().__init__(options)

    def run(self) -> None:
        self.print("outvenv")
        self.print(f"declare -f deactivate > {os.devnull} && deactivate")
        if os.getenv("VIRTUAL_ENV"):
            self.print("unset VIRTUAL_ENV")
