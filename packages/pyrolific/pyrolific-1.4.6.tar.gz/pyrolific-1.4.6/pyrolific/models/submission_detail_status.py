from enum import Enum


class SubmissionDetailStatus(str, Enum):
    ACTIVE = "ACTIVE"
    APPROVED = "APPROVED"
    AWAITING_REVIEW = "AWAITING REVIEW"
    REJECTED = "REJECTED"
    RESERVED = "RESERVED"
    RETURNED = "RETURNED"
    TIMED_OUT = "TIMED-OUT"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
