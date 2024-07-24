import os
from argparse import Namespace
from typing import Any

PREFIX = chr(2)


class BaseCommand:
    def __init__(self, options: Namespace) -> None:
        self._prefix = "_pvenv_env"
        self._options = options

    def run(self) -> None:
        msg = f"{self.__class__.__name__} must implement run"
        raise NotImplementedError(msg)

    @staticmethod
    def print(*args: str, **kwargs: Any) -> None:
        if not os.getenv("PVENV_DEBUG"):
            args = tuple(f"{PREFIX}{arg}" for arg in args)
        print(*args, **kwargs)
