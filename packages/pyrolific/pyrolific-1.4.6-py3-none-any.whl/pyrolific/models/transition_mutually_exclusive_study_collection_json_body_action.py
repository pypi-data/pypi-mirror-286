from enum import Enum


class TransitionMutuallyExclusiveStudyCollectionJsonBodyAction(str, Enum):
    CANCEL_PUBLISH = "CANCEL_PUBLISH"
    PUBLISH = "PUBLISH"
    SCHEDULE_PUBLISH = "SCHEDULE_PUBLISH"

    def __str__(self) -> str:
        return str(self.value)
