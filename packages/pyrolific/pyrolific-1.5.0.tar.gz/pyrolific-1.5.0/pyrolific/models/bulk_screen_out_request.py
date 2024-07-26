from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BulkScreenOutRequest")


@_attrs_define
class BulkScreenOutRequest:
    """
    Attributes:
        submission_ids (List[str]): List of submission ids to screen out, must belong to the study.
        bonus_per_submission (float): The bonus amount to pay per submission, in your study currency. Minimum £0.10 or
            $0.14. Example: 0.5.
    """

    submission_ids: List[str]
    bonus_per_submission: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        submission_ids = self.submission_ids

        bonus_per_submission = self.bonus_per_submission

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "submission_ids": submission_ids,
                "bonus_per_submission": bonus_per_submission,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        submission_ids = cast(List[str], d.pop("submission_ids"))

        bonus_per_submission = d.pop("bonus_per_submission")

        bulk_screen_out_request = cls(
            submission_ids=submission_ids,
            bonus_per_submission=bonus_per_submission,
        )

        bulk_screen_out_request.additional_properties = d
        return bulk_screen_out_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
