from enum import Enum


class MessageDataCategory(str, Enum):
    FEEDBACK = "feedback"
    OTHER = "other"
    PAYMENT_ISSUES = "payment-issues"
    PAYMENT_TIMING = "payment-timing"
    REJECTIONS = "rejections"
    TECHNICAL_ISSUES = "technical-issues"

    def __str__(self) -> str:
        return str(self.value)
