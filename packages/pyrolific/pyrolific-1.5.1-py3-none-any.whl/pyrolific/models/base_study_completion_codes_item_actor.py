from enum import Enum


class BaseStudyCompletionCodesItemActor(str, Enum):
    PARTICIPANT = "participant"
    RESEARCHER = "researcher"

    def __str__(self) -> str:
        return str(self.value)
