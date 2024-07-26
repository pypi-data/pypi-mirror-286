from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.subscription_event_status import SubscriptionEventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_event_payload_type_0 import SubscriptionEventPayloadType0


T = TypeVar("T", bound="SubscriptionEvent")


@_attrs_define
class SubscriptionEvent:
    """
    Attributes:
        id (Union[Unset, str]): The ID of the subscription event.
        datetime_created (Union[Unset, str]): The time the event was created.
        datetime_updated (Union[Unset, str]): The last time the event was updated.
        event_type (Union[Unset, str]): The event type that was triggered.
        resource_id (Union[Unset, str]): The Prolific Resource ID that the event is linked to.
        status (Union[Unset, SubscriptionEventStatus]): The status of the event. Will be `FAILED` if the `target_url`
            response is not 2xx.
        target_url (Union[Unset, str]): The URL where the event payload is sent.
        payload (Union['SubscriptionEventPayloadType0', None, Unset]): The event payload that was sent to the target
            url.
    """

    id: Union[Unset, str] = UNSET
    datetime_created: Union[Unset, str] = UNSET
    datetime_updated: Union[Unset, str] = UNSET
    event_type: Union[Unset, str] = UNSET
    resource_id: Union[Unset, str] = UNSET
    status: Union[Unset, SubscriptionEventStatus] = UNSET
    target_url: Union[Unset, str] = UNSET
    payload: Union["SubscriptionEventPayloadType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.subscription_event_payload_type_0 import SubscriptionEventPayloadType0

        id = self.id

        datetime_created = self.datetime_created

        datetime_updated = self.datetime_updated

        event_type = self.event_type

        resource_id = self.resource_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        target_url = self.target_url

        payload: Union[Dict[str, Any], None, Unset]
        if isinstance(self.payload, Unset):
            payload = UNSET
        elif isinstance(self.payload, SubscriptionEventPayloadType0):
            payload = self.payload.to_dict()
        else:
            payload = self.payload

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if datetime_created is not UNSET:
            field_dict["datetime_created"] = datetime_created
        if datetime_updated is not UNSET:
            field_dict["datetime_updated"] = datetime_updated
        if event_type is not UNSET:
            field_dict["event_type"] = event_type
        if resource_id is not UNSET:
            field_dict["resource_id"] = resource_id
        if status is not UNSET:
            field_dict["status"] = status
        if target_url is not UNSET:
            field_dict["target_url"] = target_url
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.subscription_event_payload_type_0 import SubscriptionEventPayloadType0

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        datetime_created = d.pop("datetime_created", UNSET)

        datetime_updated = d.pop("datetime_updated", UNSET)

        event_type = d.pop("event_type", UNSET)

        resource_id = d.pop("resource_id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, SubscriptionEventStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SubscriptionEventStatus(_status)

        target_url = d.pop("target_url", UNSET)

        def _parse_payload(data: object) -> Union["SubscriptionEventPayloadType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                payload_type_0 = SubscriptionEventPayloadType0.from_dict(data)

                return payload_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SubscriptionEventPayloadType0", None, Unset], data)

        payload = _parse_payload(d.pop("payload", UNSET))

        subscription_event = cls(
            id=id,
            datetime_created=datetime_created,
            datetime_updated=datetime_updated,
            event_type=event_type,
            resource_id=resource_id,
            status=status,
            target_url=target_url,
            payload=payload,
        )

        subscription_event.additional_properties = d
        return subscription_event

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
