from enum import Enum


class SubmissionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    APPROVED = "APPROVED"
    AWAITING_REVIEW = "AWAITING REVIEW"
    REJECTED = "REJECTED"
    RESERVED = "RESERVED"
    RETURNED = "RETURNED"
    SCREENED_OUT = "SCREENED OUT"
    TIMED_OUT = "TIMED-OUT"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
