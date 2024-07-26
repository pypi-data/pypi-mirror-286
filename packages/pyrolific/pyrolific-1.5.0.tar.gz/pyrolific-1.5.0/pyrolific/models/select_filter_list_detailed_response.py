from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.filter_list_attributes_type import FilterListAttributesType
from ..models.select_filter_list_attributes_data_type import SelectFilterListAttributesDataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.select_filter_list_attributes_choices import SelectFilterListAttributesChoices


T = TypeVar("T", bound="SelectFilterListDetailedResponse")


@_attrs_define
class SelectFilterListDetailedResponse:
    """
    Attributes:
        filter_id (Union[Unset, str]): The ID of the filter, based on a slugified version of the title at the time the
            filter was created.
        title (Union[Unset, str]): The title of the filter.
        description (Union[Unset, str]): A description of the filter.
        type (Union[Unset, FilterListAttributesType]): The filter type.
        question (Union[Unset, str]): The question asked of participants to generate this filter.
        choices (Union[Unset, SelectFilterListAttributesChoices]): An object containing all the filter's possible
            responses as key-value pairs, with sequential integer IDs or database ObjectIDs as the keys and the text of the
            response as the values.
        data_type (Union[Unset, SelectFilterListAttributesDataType]): The format of the keys in the choices object. If
            the keys are strings representing sequential integers,
            the data format is integer. If the keys are database ObjectIDs, the type of ID is specified.
        researcher_help_text (Union[None, Unset, str]): Some help text to be displayed to researchers in the
            prescreening modal.
        participant_help_text (Union[None, Unset, str]): Some help text to be displayed to participants in the About You
            section.
        category (Union[None, Unset, str]): The category the filter is displayed in in About You and the prescreening
            modal.
        subcategory (Union[None, Unset, str]): The sub-category the filter is displayed in in the prescreening modal.
        display_order (Union[None, Unset, int]): The order in which the filter is displayed within its sub-category in
            the prescreening modal.
        tags (Union[List[str], None, Unset]): Some additional tags that can be used to display the filter in a specific
            way, e.g. recommended, new, expiring.
    """

    filter_id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type: Union[Unset, FilterListAttributesType] = UNSET
    question: Union[Unset, str] = UNSET
    choices: Union[Unset, "SelectFilterListAttributesChoices"] = UNSET
    data_type: Union[Unset, SelectFilterListAttributesDataType] = UNSET
    researcher_help_text: Union[None, Unset, str] = UNSET
    participant_help_text: Union[None, Unset, str] = UNSET
    category: Union[None, Unset, str] = UNSET
    subcategory: Union[None, Unset, str] = UNSET
    display_order: Union[None, Unset, int] = UNSET
    tags: Union[List[str], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_id = self.filter_id

        title = self.title

        description = self.description

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        question = self.question

        choices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = self.choices.to_dict()

        data_type: Union[Unset, str] = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = self.data_type.value

        researcher_help_text: Union[None, Unset, str]
        if isinstance(self.researcher_help_text, Unset):
            researcher_help_text = UNSET
        else:
            researcher_help_text = self.researcher_help_text

        participant_help_text: Union[None, Unset, str]
        if isinstance(self.participant_help_text, Unset):
            participant_help_text = UNSET
        else:
            participant_help_text = self.participant_help_text

        category: Union[None, Unset, str]
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        subcategory: Union[None, Unset, str]
        if isinstance(self.subcategory, Unset):
            subcategory = UNSET
        else:
            subcategory = self.subcategory

        display_order: Union[None, Unset, int]
        if isinstance(self.display_order, Unset):
            display_order = UNSET
        else:
            display_order = self.display_order

        tags: Union[List[str], None, Unset]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_id is not UNSET:
            field_dict["filter_id"] = filter_id
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if question is not UNSET:
            field_dict["question"] = question
        if choices is not UNSET:
            field_dict["choices"] = choices
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if researcher_help_text is not UNSET:
            field_dict["researcher_help_text"] = researcher_help_text
        if participant_help_text is not UNSET:
            field_dict["participant_help_text"] = participant_help_text
        if category is not UNSET:
            field_dict["category"] = category
        if subcategory is not UNSET:
            field_dict["subcategory"] = subcategory
        if display_order is not UNSET:
            field_dict["display_order"] = display_order
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.select_filter_list_attributes_choices import SelectFilterListAttributesChoices

        d = src_dict.copy()
        filter_id = d.pop("filter_id", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, FilterListAttributesType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = FilterListAttributesType(_type)

        question = d.pop("question", UNSET)

        _choices = d.pop("choices", UNSET)
        choices: Union[Unset, SelectFilterListAttributesChoices]
        if isinstance(_choices, Unset):
            choices = UNSET
        else:
            choices = SelectFilterListAttributesChoices.from_dict(_choices)

        _data_type = d.pop("data_type", UNSET)
        data_type: Union[Unset, SelectFilterListAttributesDataType]
        if isinstance(_data_type, Unset):
            data_type = UNSET
        else:
            data_type = SelectFilterListAttributesDataType(_data_type)

        def _parse_researcher_help_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        researcher_help_text = _parse_researcher_help_text(d.pop("researcher_help_text", UNSET))

        def _parse_participant_help_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        participant_help_text = _parse_participant_help_text(d.pop("participant_help_text", UNSET))

        def _parse_category(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_subcategory(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subcategory = _parse_subcategory(d.pop("subcategory", UNSET))

        def _parse_display_order(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        display_order = _parse_display_order(d.pop("display_order", UNSET))

        def _parse_tags(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(List[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        select_filter_list_detailed_response = cls(
            filter_id=filter_id,
            title=title,
            description=description,
            type=type,
            question=question,
            choices=choices,
            data_type=data_type,
            researcher_help_text=researcher_help_text,
            participant_help_text=participant_help_text,
            category=category,
            subcategory=subcategory,
            display_order=display_order,
            tags=tags,
        )

        select_filter_list_detailed_response.additional_properties = d
        return select_filter_list_detailed_response

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
