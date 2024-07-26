from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessDetailProgress")


@_attrs_define
class AccessDetailProgress:
    """
    Attributes:
        external_url (str): URL of the task you want to send the participant to. You can pass URL search parameters as
            in `external_study_url`.
        total_allocation (float): The number of places you want to be sent to this URL for taskflow.
        allocated (Union[Unset, float]): The number of places that have been allocated to participants.
    """

    external_url: str
    total_allocation: float
    allocated: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_url = self.external_url

        total_allocation = self.total_allocation

        allocated = self.allocated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "external_url": external_url,
                "total_allocation": total_allocation,
            }
        )
        if allocated is not UNSET:
            field_dict["allocated"] = allocated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        external_url = d.pop("external_url")

        total_allocation = d.pop("total_allocation")

        allocated = d.pop("allocated", UNSET)

        access_detail_progress = cls(
            external_url=external_url,
            total_allocation=total_allocation,
            allocated=allocated,
        )

        access_detail_progress.additional_properties = d
        return access_detail_progress

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
