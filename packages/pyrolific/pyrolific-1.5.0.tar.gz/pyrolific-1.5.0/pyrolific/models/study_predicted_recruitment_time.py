from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StudyPredictedRecruitmentTime")


@_attrs_define
class StudyPredictedRecruitmentTime:
    """
    Attributes:
        precise_recruitment_time_hours (Union[Unset, float]): The predicted recruitment time in hours Example: 2.13.
        lower_bound_hours (Union[Unset, float]): The lower bound of the predicted recruitment time in hours Example:
            1.5.
        upper_bound_hours (Union[Unset, float]): The upper bound of the predicted recruitment time in hours Example:
            2.5.
        display_string (Union[Unset, str]): A human-readable string representing the predicted recruitment time Example:
            1 hour 23 minutes.
        limit_at (Union[Unset, float]): The limit at which the accuracy of the prediction becomes unstable.
            This should be used when rendering the recruitment times in a GUI. For example if the limit_at is 10,
            and the predicted recruitment time is 12 hours, the display string should be "10 hours+". This
            has been done for you in the display_string field.
    """

    precise_recruitment_time_hours: Union[Unset, float] = UNSET
    lower_bound_hours: Union[Unset, float] = UNSET
    upper_bound_hours: Union[Unset, float] = UNSET
    display_string: Union[Unset, str] = UNSET
    limit_at: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        precise_recruitment_time_hours = self.precise_recruitment_time_hours

        lower_bound_hours = self.lower_bound_hours

        upper_bound_hours = self.upper_bound_hours

        display_string = self.display_string

        limit_at = self.limit_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if precise_recruitment_time_hours is not UNSET:
            field_dict["precise_recruitment_time_hours"] = precise_recruitment_time_hours
        if lower_bound_hours is not UNSET:
            field_dict["lower_bound_hours"] = lower_bound_hours
        if upper_bound_hours is not UNSET:
            field_dict["upper_bound_hours"] = upper_bound_hours
        if display_string is not UNSET:
            field_dict["display_string"] = display_string
        if limit_at is not UNSET:
            field_dict["limit_at"] = limit_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        precise_recruitment_time_hours = d.pop("precise_recruitment_time_hours", UNSET)

        lower_bound_hours = d.pop("lower_bound_hours", UNSET)

        upper_bound_hours = d.pop("upper_bound_hours", UNSET)

        display_string = d.pop("display_string", UNSET)

        limit_at = d.pop("limit_at", UNSET)

        study_predicted_recruitment_time = cls(
            precise_recruitment_time_hours=precise_recruitment_time_hours,
            lower_bound_hours=lower_bound_hours,
            upper_bound_hours=upper_bound_hours,
            display_string=display_string,
            limit_at=limit_at,
        )

        study_predicted_recruitment_time.additional_properties = d
        return study_predicted_recruitment_time

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
