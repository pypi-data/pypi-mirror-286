from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.study_cost_breakdown import StudyCostBreakdown
    from ..models.study_total_cost_links import StudyTotalCostLinks
    from ..models.study_total_cost_rewards import StudyTotalCostRewards


T = TypeVar("T", bound="StudyTotalCost")


@_attrs_define
class StudyTotalCost:
    """
    Attributes:
        rewards (Union[Unset, StudyTotalCostRewards]):
        bonuses (Union[Unset, StudyCostBreakdown]):
        field_links (Union[Unset, StudyTotalCostLinks]):
    """

    rewards: Union[Unset, "StudyTotalCostRewards"] = UNSET
    bonuses: Union[Unset, "StudyCostBreakdown"] = UNSET
    field_links: Union[Unset, "StudyTotalCostLinks"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rewards: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rewards, Unset):
            rewards = self.rewards.to_dict()

        bonuses: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bonuses, Unset):
            bonuses = self.bonuses.to_dict()

        field_links: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = self.field_links.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rewards is not UNSET:
            field_dict["rewards"] = rewards
        if bonuses is not UNSET:
            field_dict["bonuses"] = bonuses
        if field_links is not UNSET:
            field_dict["_links"] = field_links

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.study_cost_breakdown import StudyCostBreakdown
        from ..models.study_total_cost_links import StudyTotalCostLinks
        from ..models.study_total_cost_rewards import StudyTotalCostRewards

        d = src_dict.copy()
        _rewards = d.pop("rewards", UNSET)
        rewards: Union[Unset, StudyTotalCostRewards]
        if isinstance(_rewards, Unset):
            rewards = UNSET
        else:
            rewards = StudyTotalCostRewards.from_dict(_rewards)

        _bonuses = d.pop("bonuses", UNSET)
        bonuses: Union[Unset, StudyCostBreakdown]
        if isinstance(_bonuses, Unset):
            bonuses = UNSET
        else:
            bonuses = StudyCostBreakdown.from_dict(_bonuses)

        _field_links = d.pop("_links", UNSET)
        field_links: Union[Unset, StudyTotalCostLinks]
        if isinstance(_field_links, Unset):
            field_links = UNSET
        else:
            field_links = StudyTotalCostLinks.from_dict(_field_links)

        study_total_cost = cls(
            rewards=rewards,
            bonuses=bonuses,
            field_links=field_links,
        )

        study_total_cost.additional_properties = d
        return study_total_cost

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
