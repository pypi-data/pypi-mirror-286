from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

from pvenv.subcommands.base import BaseCommand

if TYPE_CHECKING:
    from argparse import Namespace
    from pathlib import Path


class Command(BaseCommand):
    def __init__(self, options: Namespace) -> None:
        super().__init__(options)
        self.base_dir: Path = options.base_dir
        self.venv_to_remove: list[str] = options.venvs_to_remove

    def run(self) -> None:
        for venv in self.venv_to_remove:
            venv_path = self.base_dir.joinpath(venv)
            if not venv_path.exists():
                print(f"{venv} does not exist, skipping...")
                continue
            try:
                shutil.rmtree(venv_path)
            except (PermissionError, NotADirectoryError):
                print(f"Cannot delete {venv}, skipping...")
                continue

            print(f"{venv} removed successfully!")
