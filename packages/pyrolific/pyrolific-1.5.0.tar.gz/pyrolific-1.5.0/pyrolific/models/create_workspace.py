from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkspace")


@_attrs_define
class CreateWorkspace:
    """
    Attributes:
        title (str): Name of workspace
        naivety_distribution_rate (Union[None, Unset, float]): Control the balance between speed of your studies and the
            naivety of the participants.

            If not defined, by default Prolific calculates the best rate for most studies
            taking into account the `filters` and the `total_available_places` needed for this study.

            Use 0 if your priority is speed. When this property is set to 0 all eligible participants will have access
            to your study at the same time, without any prioritization.

            You can also set this at a project and study level.
        currency_code (Union[Unset, str]): Currency used for all transactions within the workspace. Must be GBP or USD.
    """

    title: str
    naivety_distribution_rate: Union[None, Unset, float] = UNSET
    currency_code: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title

        naivety_distribution_rate: Union[None, Unset, float]
        if isinstance(self.naivety_distribution_rate, Unset):
            naivety_distribution_rate = UNSET
        else:
            naivety_distribution_rate = self.naivety_distribution_rate

        currency_code = self.currency_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if naivety_distribution_rate is not UNSET:
            field_dict["naivety_distribution_rate"] = naivety_distribution_rate
        if currency_code is not UNSET:
            field_dict["currency_code"] = currency_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        def _parse_naivety_distribution_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        naivety_distribution_rate = _parse_naivety_distribution_rate(d.pop("naivety_distribution_rate", UNSET))

        currency_code = d.pop("currency_code", UNSET)

        create_workspace = cls(
            title=title,
            naivety_distribution_rate=naivety_distribution_rate,
            currency_code=currency_code,
        )

        create_workspace.additional_properties = d
        return create_workspace

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
