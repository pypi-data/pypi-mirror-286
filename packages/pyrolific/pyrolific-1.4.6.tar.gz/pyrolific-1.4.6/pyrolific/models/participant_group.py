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
    from ..models.participant_group_feeder_studies_item import (
        ParticipantGroupFeederStudiesItem,
    )


T = TypeVar("T", bound="ParticipantGroup")


@_attrs_define
class ParticipantGroup:
    """
    Attributes:
        id (Union[Unset, str]): The id of the participant group Example: 5e9b9c9b0f9c9a0001b0b1f5.
        name (Union[Unset, str]): The name of the participant group Example: Group 1.
        project_id (Union[Unset, None, str]): The id of the project the participant group belongs to
        workspace_id (Union[Unset, None, str]): The id of the workspace the participant group belongs to. A participant
            group can only belong to either a workspace or an organisation. Example: 5e9b9c9b0f9c9a0001b1ca2f.
        organisation_id (Union[Unset, None, str]): The id of the organisation the participant group belongs to. A
            participant group can only belong to either a workspace or an organisation. Example: 5e9b9c9b0f9c9a0001b1ca2f.
        description (Union[Unset, None, str]): The user-provided description of the participant group Example: My first
            participant group.
        participant_count (Union[Unset, int]): The number of participants in the participant group Example: 10.
        is_deleted (Union[Unset, bool]): Whether the participant group has been deleted
        feeder_studies (Union[Unset, List['ParticipantGroupFeederStudiesItem']]): Details of all studies which are
            configured to modify the participants in this group through completion codes.
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    project_id: Union[Unset, None, str] = UNSET
    workspace_id: Union[Unset, None, str] = UNSET
    organisation_id: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    participant_count: Union[Unset, int] = UNSET
    is_deleted: Union[Unset, bool] = UNSET
    feeder_studies: Union[Unset, List["ParticipantGroupFeederStudiesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        project_id = self.project_id
        workspace_id = self.workspace_id
        organisation_id = self.organisation_id
        description = self.description
        participant_count = self.participant_count
        is_deleted = self.is_deleted
        feeder_studies: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.feeder_studies, Unset):
            feeder_studies = []
            for feeder_studies_item_data in self.feeder_studies:
                feeder_studies_item = feeder_studies_item_data.to_dict()

                feeder_studies.append(feeder_studies_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if organisation_id is not UNSET:
            field_dict["organisation_id"] = organisation_id
        if description is not UNSET:
            field_dict["description"] = description
        if participant_count is not UNSET:
            field_dict["participant_count"] = participant_count
        if is_deleted is not UNSET:
            field_dict["is_deleted"] = is_deleted
        if feeder_studies is not UNSET:
            field_dict["feeder_studies"] = feeder_studies

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.participant_group_feeder_studies_item import (
            ParticipantGroupFeederStudiesItem,
        )

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        project_id = d.pop("project_id", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        organisation_id = d.pop("organisation_id", UNSET)

        description = d.pop("description", UNSET)

        participant_count = d.pop("participant_count", UNSET)

        is_deleted = d.pop("is_deleted", UNSET)

        feeder_studies = []
        _feeder_studies = d.pop("feeder_studies", UNSET)
        for feeder_studies_item_data in _feeder_studies or []:
            feeder_studies_item = ParticipantGroupFeederStudiesItem.from_dict(
                feeder_studies_item_data
            )

            feeder_studies.append(feeder_studies_item)

        participant_group = cls(
            id=id,
            name=name,
            project_id=project_id,
            workspace_id=workspace_id,
            organisation_id=organisation_id,
            description=description,
            participant_count=participant_count,
            is_deleted=is_deleted,
            feeder_studies=feeder_studies,
        )

        participant_group.additional_properties = d
        return participant_group

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
