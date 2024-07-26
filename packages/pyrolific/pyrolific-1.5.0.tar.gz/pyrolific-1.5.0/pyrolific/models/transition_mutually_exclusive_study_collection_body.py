from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transition_mutually_exclusive_study_collection_body_action import (
    TransitionMutuallyExclusiveStudyCollectionBodyAction,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TransitionMutuallyExclusiveStudyCollectionBody")


@_attrs_define
class TransitionMutuallyExclusiveStudyCollectionBody:
    """
    Attributes:
        action (Union[Unset, TransitionMutuallyExclusiveStudyCollectionBodyAction]):
        publish_at (Union[Unset, str]): Optional parameter for scheduling publish, indicating the datetime and timezone
            the study collection should be scheduled to be published at
    """

    action: Union[Unset, TransitionMutuallyExclusiveStudyCollectionBodyAction] = UNSET
    publish_at: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action: Union[Unset, str] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.value

        publish_at = self.publish_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if publish_at is not UNSET:
            field_dict["publish_at"] = publish_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _action = d.pop("action", UNSET)
        action: Union[Unset, TransitionMutuallyExclusiveStudyCollectionBodyAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = TransitionMutuallyExclusiveStudyCollectionBodyAction(_action)

        publish_at = d.pop("publish_at", UNSET)

        transition_mutually_exclusive_study_collection_body = cls(
            action=action,
            publish_at=publish_at,
        )

        transition_mutually_exclusive_study_collection_body.additional_properties = d
        return transition_mutually_exclusive_study_collection_body

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
