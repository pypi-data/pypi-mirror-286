from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.message_data_category import MessageDataCategory
from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="MessageData")


@_attrs_define
class MessageData:
    """Metadata for a message

    Attributes:
        study_id (Union[Unset, str]): What study the message relates to. In case this is not automatically filled for
            the participant, they can choose which study their message relates to. Example: 620ca2735fcbba4fa2b3211a.
        category (Union[Unset, MessageDataCategory]): Participants can self-categorise their message before sending it.
            Example: feedback.
    """

    study_id: Union[Unset, str] = UNSET
    category: Union[Unset, MessageDataCategory] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        study_id = self.study_id
        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if study_id is not UNSET:
            field_dict["study_id"] = study_id
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        study_id = d.pop("study_id", UNSET)

        _category = d.pop("category", UNSET)
        category: Union[Unset, MessageDataCategory]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = MessageDataCategory(_category)

        message_data = cls(
            study_id=study_id,
            category=category,
        )

        message_data.additional_properties = d
        return message_data

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
