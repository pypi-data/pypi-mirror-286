import os
from argparse import Namespace

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace) -> None:
        super().__init__(options)

    def run(self) -> None:
        if self._prefix not in os.environ:
            return

        self.print(f"unset {self._prefix}")
        prefix_size = len(self._prefix) + 1
        unset_prefix_size = len(self._prefix) + len("_unset") + 1
        for key, value in os.environ.items():
            if key.startswith(f"{self._prefix}_"):
                if key.startswith(f"{self._prefix}_unset_"):
                    self.print(f"unset {key[unset_prefix_size:]}")
                else:
                    self.print(f"export {key[prefix_size:]}={value}")
                self.print(f"unset {key}")
