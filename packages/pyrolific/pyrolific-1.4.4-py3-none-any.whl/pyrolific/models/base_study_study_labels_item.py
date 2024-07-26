from enum import Enum


class BaseStudyStudyLabelsItem(str, Enum):
    ANNOTATION = "annotation"
    INTERVIEW = "interview"
    OTHER = "other"
    SURVEY = "survey"
    WRITING_TASK = "writing_task"

    def __str__(self) -> str:
        return str(self.value)
