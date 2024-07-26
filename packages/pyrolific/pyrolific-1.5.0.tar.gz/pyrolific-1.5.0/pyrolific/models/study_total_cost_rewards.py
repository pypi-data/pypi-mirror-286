from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.amount_and_currency import AmountAndCurrency


T = TypeVar("T", bound="StudyTotalCostRewards")


@_attrs_define
class StudyTotalCostRewards:
    """
    Attributes:
        rewards (Union[Unset, AmountAndCurrency]):
        fees (Union[Unset, AmountAndCurrency]):
        tax (Union[Unset, AmountAndCurrency]):
        rep_sample_fees (Union[Unset, AmountAndCurrency]):
        rep_sample_tax (Union[Unset, AmountAndCurrency]):
    """

    rewards: Union[Unset, "AmountAndCurrency"] = UNSET
    fees: Union[Unset, "AmountAndCurrency"] = UNSET
    tax: Union[Unset, "AmountAndCurrency"] = UNSET
    rep_sample_fees: Union[Unset, "AmountAndCurrency"] = UNSET
    rep_sample_tax: Union[Unset, "AmountAndCurrency"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rewards: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rewards, Unset):
            rewards = self.rewards.to_dict()

        fees: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fees, Unset):
            fees = self.fees.to_dict()

        tax: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tax, Unset):
            tax = self.tax.to_dict()

        rep_sample_fees: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rep_sample_fees, Unset):
            rep_sample_fees = self.rep_sample_fees.to_dict()

        rep_sample_tax: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rep_sample_tax, Unset):
            rep_sample_tax = self.rep_sample_tax.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rewards is not UNSET:
            field_dict["rewards"] = rewards
        if fees is not UNSET:
            field_dict["fees"] = fees
        if tax is not UNSET:
            field_dict["tax"] = tax
        if rep_sample_fees is not UNSET:
            field_dict["rep_sample_fees"] = rep_sample_fees
        if rep_sample_tax is not UNSET:
            field_dict["rep_sample_tax"] = rep_sample_tax

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.amount_and_currency import AmountAndCurrency

        d = src_dict.copy()
        _rewards = d.pop("rewards", UNSET)
        rewards: Union[Unset, AmountAndCurrency]
        if isinstance(_rewards, Unset):
            rewards = UNSET
        else:
            rewards = AmountAndCurrency.from_dict(_rewards)

        _fees = d.pop("fees", UNSET)
        fees: Union[Unset, AmountAndCurrency]
        if isinstance(_fees, Unset):
            fees = UNSET
        else:
            fees = AmountAndCurrency.from_dict(_fees)

        _tax = d.pop("tax", UNSET)
        tax: Union[Unset, AmountAndCurrency]
        if isinstance(_tax, Unset):
            tax = UNSET
        else:
            tax = AmountAndCurrency.from_dict(_tax)

        _rep_sample_fees = d.pop("rep_sample_fees", UNSET)
        rep_sample_fees: Union[Unset, AmountAndCurrency]
        if isinstance(_rep_sample_fees, Unset):
            rep_sample_fees = UNSET
        else:
            rep_sample_fees = AmountAndCurrency.from_dict(_rep_sample_fees)

        _rep_sample_tax = d.pop("rep_sample_tax", UNSET)
        rep_sample_tax: Union[Unset, AmountAndCurrency]
        if isinstance(_rep_sample_tax, Unset):
            rep_sample_tax = UNSET
        else:
            rep_sample_tax = AmountAndCurrency.from_dict(_rep_sample_tax)

        study_total_cost_rewards = cls(
            rewards=rewards,
            fees=fees,
            tax=tax,
            rep_sample_fees=rep_sample_fees,
            rep_sample_tax=rep_sample_tax,
        )

        study_total_cost_rewards.additional_properties = d
        return study_total_cost_rewards

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
