from typing import Any, Dict, Type, TypeVar


from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast, List
from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="MutuallyExclusiveStudyCollectionUpdate")


@_attrs_define
class MutuallyExclusiveStudyCollectionUpdate:
    """
    Attributes:
        name (Union[Unset, str]): Mutually exclusive study collection name Example: My Mutually Exclusive Study
            Collection.
        description (Union[Unset, str]): A description of the study collection Example: This is a description of my
            mutually exclusive study collection.
        publish_at (Union[Unset, None, str]): Datetime and timezone the study collection should be scheduled to be
            published at Example: 2050-02-28T13:45:00 Europe/London.
        study_ids (Union[Unset, List[str]]): List of study ids you wish to include in the collection. Note, this will
            overwrite the current list of studies in the collection
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    publish_at: Union[Unset, None, str] = UNSET
    study_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        publish_at = self.publish_at
        study_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.study_ids, Unset):
            study_ids = self.study_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if publish_at is not UNSET:
            field_dict["publish_at"] = publish_at
        if study_ids is not UNSET:
            field_dict["study_ids"] = study_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        publish_at = d.pop("publish_at", UNSET)

        study_ids = cast(List[str], d.pop("study_ids", UNSET))

        mutually_exclusive_study_collection_update = cls(
            name=name,
            description=description,
            publish_at=publish_at,
            study_ids=study_ids,
        )

        return mutually_exclusive_study_collection_update
