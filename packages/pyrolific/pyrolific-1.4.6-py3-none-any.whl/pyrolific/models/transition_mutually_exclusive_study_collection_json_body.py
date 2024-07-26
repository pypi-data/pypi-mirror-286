from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.transition_mutually_exclusive_study_collection_json_body_action import (
    TransitionMutuallyExclusiveStudyCollectionJsonBodyAction,
)
from ..types import UNSET, Unset


T = TypeVar("T", bound="TransitionMutuallyExclusiveStudyCollectionJsonBody")


@_attrs_define
class TransitionMutuallyExclusiveStudyCollectionJsonBody:
    """
    Attributes:
        action (Union[Unset, TransitionMutuallyExclusiveStudyCollectionJsonBodyAction]):
        publish_at (Union[Unset, str]): Optional parameter for scheduling publish, indicating the datetime and timezone
            the study collection should be scheduled to be published at
    """

    action: Union[
        Unset, TransitionMutuallyExclusiveStudyCollectionJsonBodyAction
    ] = UNSET
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
        action: Union[Unset, TransitionMutuallyExclusiveStudyCollectionJsonBodyAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = TransitionMutuallyExclusiveStudyCollectionJsonBodyAction(_action)

        publish_at = d.pop("publish_at", UNSET)

        transition_mutually_exclusive_study_collection_json_body = cls(
            action=action,
            publish_at=publish_at,
        )

        transition_mutually_exclusive_study_collection_json_body.additional_properties = d
        return transition_mutually_exclusive_study_collection_json_body

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
