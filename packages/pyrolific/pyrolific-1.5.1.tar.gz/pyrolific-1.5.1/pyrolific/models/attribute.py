from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attribute_value_type_0_type_0 import AttributeValueType0Type0
    from ..models.attribute_value_type_1_type_0_item_type_1 import AttributeValueType1Type0ItemType1


T = TypeVar("T", bound="Attribute")


@_attrs_define
class Attribute:
    """
    Attributes:
        value (Union['AttributeValueType0Type0', List[Union['AttributeValueType1Type0ItemType1', str]], None, bool,
            float, str]): Attribute value. It can be null, a number, a date or a boolean depending on the type of
            requirement.
            For boolean values, there is no need to specify all false (non selected) options. Example: true.
        index (Union[Unset, float]): Attribute index. It is mandatory for some type of requirements,
            like SelectAnswerEligibilityRequirement. Example: 5.0.
        name (Union[Unset, str]): Attribute name. It is mandatory for some type of requirements,
            like AgeRangeEligibilityRequirement.
    """

    value: Union[
        "AttributeValueType0Type0", List[Union["AttributeValueType1Type0ItemType1", str]], None, bool, float, str
    ]
    index: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.attribute_value_type_0_type_0 import AttributeValueType0Type0
        from ..models.attribute_value_type_1_type_0_item_type_1 import AttributeValueType1Type0ItemType1

        value: Union[Dict[str, Any], List[Union[Dict[str, Any], str]], None, bool, float, str]
        if isinstance(self.value, AttributeValueType0Type0):
            value = self.value.to_dict()
        elif isinstance(self.value, list):
            value = []
            for value_type_1_type_0_item_data in self.value:
                value_type_1_type_0_item: Union[Dict[str, Any], str]
                if isinstance(value_type_1_type_0_item_data, AttributeValueType1Type0ItemType1):
                    value_type_1_type_0_item = value_type_1_type_0_item_data.to_dict()
                else:
                    value_type_1_type_0_item = value_type_1_type_0_item_data
                value.append(value_type_1_type_0_item)

        else:
            value = self.value

        index = self.index

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if index is not UNSET:
            field_dict["index"] = index
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.attribute_value_type_0_type_0 import AttributeValueType0Type0
        from ..models.attribute_value_type_1_type_0_item_type_1 import AttributeValueType1Type0ItemType1

        d = src_dict.copy()

        def _parse_value(
            data: object,
        ) -> Union[
            "AttributeValueType0Type0", List[Union["AttributeValueType1Type0ItemType1", str]], None, bool, float, str
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0_type_0 = AttributeValueType0Type0.from_dict(data)

                return value_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1_type_0 = []
                _value_type_1_type_0 = data
                for value_type_1_type_0_item_data in _value_type_1_type_0:

                    def _parse_value_type_1_type_0_item(
                        data: object,
                    ) -> Union["AttributeValueType1Type0ItemType1", str]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_1_type_0_item_type_1 = AttributeValueType1Type0ItemType1.from_dict(data)

                            return value_type_1_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        return cast(Union["AttributeValueType1Type0ItemType1", str], data)

                    value_type_1_type_0_item = _parse_value_type_1_type_0_item(value_type_1_type_0_item_data)

                    value_type_1_type_0.append(value_type_1_type_0_item)

                return value_type_1_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "AttributeValueType0Type0",
                    List[Union["AttributeValueType1Type0ItemType1", str]],
                    None,
                    bool,
                    float,
                    str,
                ],
                data,
            )

        value = _parse_value(d.pop("value"))

        index = d.pop("index", UNSET)

        name = d.pop("name", UNSET)

        attribute = cls(
            value=value,
            index=index,
            name=name,
        )

        attribute.additional_properties = d
        return attribute

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
