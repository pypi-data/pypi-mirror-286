import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_data import MessageData


T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """
    Attributes:
        sender_id (str): Id of the user who sent the message
        body (str): Body of the message.
        sent_at (datetime.datetime): Date time when message was sent
        channel_id (str): The channel ID, for linking back to a thread in the Prolific app. Example:
            d45c8a5e812ff990fc6546beaf888c9820f4c184f7200a45d900cf0f321f7f38.
        type (Union[Unset, str]): Will only me message for now
        data (Union[Unset, MessageData]): Metadata for a message
    """

    sender_id: str
    body: str
    sent_at: datetime.datetime
    channel_id: str
    type: Union[Unset, str] = UNSET
    data: Union[Unset, "MessageData"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sender_id = self.sender_id

        body = self.body

        sent_at = self.sent_at.isoformat()

        channel_id = self.channel_id

        type = self.type

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sender_id": sender_id,
                "body": body,
                "sent_at": sent_at,
                "channel_id": channel_id,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_data import MessageData

        d = src_dict.copy()
        sender_id = d.pop("sender_id")

        body = d.pop("body")

        sent_at = isoparse(d.pop("sent_at"))

        channel_id = d.pop("channel_id")

        type = d.pop("type", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, MessageData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = MessageData.from_dict(_data)

        message = cls(
            sender_id=sender_id,
            body=body,
            sent_at=sent_at,
            channel_id=channel_id,
            type=type,
            data=data,
        )

        message.additional_properties = d
        return message

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
