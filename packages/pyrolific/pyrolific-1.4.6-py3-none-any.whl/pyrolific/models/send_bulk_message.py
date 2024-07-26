from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, List


T = TypeVar("T", bound="SendBulkMessage")


@_attrs_define
class SendBulkMessage:
    """
    Attributes:
        ids (List[str]): A list of participant ID's
        body (str): Message Body. Text is sanitised for safe storage and display.
        study_id (str): A study ID
    """

    ids: List[str]
    body: str
    study_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ids = self.ids

        body = self.body
        study_id = self.study_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ids": ids,
                "body": body,
                "study_id": study_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ids = cast(List[str], d.pop("ids"))

        body = d.pop("body")

        study_id = d.pop("study_id")

        send_bulk_message = cls(
            ids=ids,
            body=body,
            study_id=study_id,
        )

        send_bulk_message.additional_properties = d
        return send_bulk_message

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
