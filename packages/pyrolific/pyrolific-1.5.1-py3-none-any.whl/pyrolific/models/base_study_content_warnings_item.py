from enum import Enum


class BaseStudyContentWarningsItem(str, Enum):
    EXPLICIT = "explicit"
    SENSITIVE = "sensitive"

    def __str__(self) -> str:
        return str(self.value)
