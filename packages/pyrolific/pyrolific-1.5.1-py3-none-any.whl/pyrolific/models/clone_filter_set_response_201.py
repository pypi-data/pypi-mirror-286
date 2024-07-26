from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.range_filter import RangeFilter
    from ..models.select_filter import SelectFilter


T = TypeVar("T", bound="CloneFilterSetResponse201")


@_attrs_define
class CloneFilterSetResponse201:
    """
    Attributes:
        id (Union[Unset, str]): ID of the filter set.
        version (Union[Unset, int]): An incrementing integer indicating the version of the filter set.
        is_deleted (Union[Unset, bool]): Whether the filter set has been deleted.
        is_locked (Union[Unset, bool]): Whether the filter set has been locked.
        workspace_id (Union[None, Unset, str]): ID of the workspace where the filter set can be used.
        organisation_id (Union[None, Unset, str]): ID of the workspace where the filter set can be used.
        name (Union[Unset, str]): Name of the filter set.
        filters (Union[Unset, List[Union['RangeFilter', 'SelectFilter']]]): List of all filters contained in the filter
            set.
        eligible_participant_count (Union[Unset, int]): The number of participants who match the filter sets filters.
            Please note that if the number is
            lower than 25 the count will be obscured to prevent identification of participants.
    """

    id: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    is_deleted: Union[Unset, bool] = UNSET
    is_locked: Union[Unset, bool] = UNSET
    workspace_id: Union[None, Unset, str] = UNSET
    organisation_id: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    filters: Union[Unset, List[Union["RangeFilter", "SelectFilter"]]] = UNSET
    eligible_participant_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.select_filter import SelectFilter

        id = self.id

        version = self.version

        is_deleted = self.is_deleted

        is_locked = self.is_locked

        workspace_id: Union[None, Unset, str]
        if isinstance(self.workspace_id, Unset):
            workspace_id = UNSET
        else:
            workspace_id = self.workspace_id

        organisation_id: Union[None, Unset, str]
        if isinstance(self.organisation_id, Unset):
            organisation_id = UNSET
        else:
            organisation_id = self.organisation_id

        name = self.name

        filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: Dict[str, Any]
                if isinstance(filters_item_data, SelectFilter):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        eligible_participant_count = self.eligible_participant_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if version is not UNSET:
            field_dict["version"] = version
        if is_deleted is not UNSET:
            field_dict["is_deleted"] = is_deleted
        if is_locked is not UNSET:
            field_dict["is_locked"] = is_locked
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if organisation_id is not UNSET:
            field_dict["organisation_id"] = organisation_id
        if name is not UNSET:
            field_dict["name"] = name
        if filters is not UNSET:
            field_dict["filters"] = filters
        if eligible_participant_count is not UNSET:
            field_dict["eligible_participant_count"] = eligible_participant_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.range_filter import RangeFilter
        from ..models.select_filter import SelectFilter

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        version = d.pop("version", UNSET)

        is_deleted = d.pop("is_deleted", UNSET)

        is_locked = d.pop("is_locked", UNSET)

        def _parse_workspace_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workspace_id = _parse_workspace_id(d.pop("workspace_id", UNSET))

        def _parse_organisation_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        organisation_id = _parse_organisation_id(d.pop("organisation_id", UNSET))

        name = d.pop("name", UNSET)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(data: object) -> Union["RangeFilter", "SelectFilter"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = SelectFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_1 = RangeFilter.from_dict(data)

                return filters_item_type_1

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        eligible_participant_count = d.pop("eligible_participant_count", UNSET)

        clone_filter_set_response_201 = cls(
            id=id,
            version=version,
            is_deleted=is_deleted,
            is_locked=is_locked,
            workspace_id=workspace_id,
            organisation_id=organisation_id,
            name=name,
            filters=filters,
            eligible_participant_count=eligible_participant_count,
        )

        clone_filter_set_response_201.additional_properties = d
        return clone_filter_set_response_201

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
