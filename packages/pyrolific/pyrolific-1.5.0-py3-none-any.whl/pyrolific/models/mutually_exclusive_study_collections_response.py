from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.mutually_exclusive_study_collection_update import MutuallyExclusiveStudyCollectionUpdate


T = TypeVar("T", bound="MutuallyExclusiveStudyCollectionsResponse")


@_attrs_define
class MutuallyExclusiveStudyCollectionsResponse:
    """
    Attributes:
        results (List['MutuallyExclusiveStudyCollectionUpdate']): List of all mutually exclusive study collections in a
            project
    """

    results: List["MutuallyExclusiveStudyCollectionUpdate"]

    def to_dict(self) -> Dict[str, Any]:
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.mutually_exclusive_study_collection_update import MutuallyExclusiveStudyCollectionUpdate

        d = src_dict.copy()
        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = MutuallyExclusiveStudyCollectionUpdate.from_dict(results_item_data)

            results.append(results_item)

        mutually_exclusive_study_collections_response = cls(
            results=results,
        )

        return mutually_exclusive_study_collections_response
