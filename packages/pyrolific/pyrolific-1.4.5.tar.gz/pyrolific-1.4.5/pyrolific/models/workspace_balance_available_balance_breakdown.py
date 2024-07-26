from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="WorkspaceBalanceAvailableBalanceBreakdown")


@_attrs_define
class WorkspaceBalanceAvailableBalanceBreakdown:
    """A breakdown of the available balance of the workspace into:
    - Funds available to pay to participants
    - Funds pre-paid to Prolific for our services
    - Funds for any VAT applied to our service fees

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_balance_available_balance_breakdown = cls()

        workspace_balance_available_balance_breakdown.additional_properties = d
        return workspace_balance_available_balance_breakdown

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
