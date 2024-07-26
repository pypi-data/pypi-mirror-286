from pathlib import Path

from iccore.project import Version


class Repo:
    def __init__(self, path: Path, version: Version = Version()) -> None:
        self.path = path
        self.version = version

    def get_version(self) -> Version:
        return self.version

    def bump_version(self, bump_type: str):
        pass
