from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import List
from ..types import UNSET, Unset
from typing import Dict

if TYPE_CHECKING:
    from ..models.secret_detail import SecretDetail


T = TypeVar("T", bound="SecretList")


@_attrs_define
class SecretList:
    """
    Example:
        [{'id': '63722971f9cc073ecc730f6a', 'value': 'secret-and-safe', 'workspace_id': '63722982f9cc073ecc730f6b'}]

    Attributes:
        results (Union[Unset, List['SecretDetail']]): A list of secrets.
    """

    results: Union[Unset, List["SecretDetail"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.secret_detail import SecretDetail

        d = src_dict.copy()
        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = SecretDetail.from_dict(results_item_data)

            results.append(results_item)

        secret_list = cls(
            results=results,
        )

        secret_list.additional_properties = d
        return secret_list

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
