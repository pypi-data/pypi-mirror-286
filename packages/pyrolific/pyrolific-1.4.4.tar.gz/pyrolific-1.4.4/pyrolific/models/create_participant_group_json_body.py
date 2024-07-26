from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, List
from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="CreateParticipantGroupJsonBody")


@_attrs_define
class CreateParticipantGroupJsonBody:
    """
    Attributes:
        name (str): The name of the participant group Example: Group 1.
        workspace_id (Union[Unset, str]): The id of the workspace to create the participant group in. Either a workspace
            or organisation ID must be specified.
        organisation_id (Union[Unset, str]): The id of the organisation to create the participant group in. Either a
            workspace or organisation ID must be specified.
        description (Union[Unset, str]): A description of the participant group Example: Participants with confirmed
            special dietary requirements..
        participant_ids (Union[Unset, List[str]]): The ids of participants to be initially added to the group Example:
            ['5e9b9c9b0f9c9a0001b0b1f4', '5e9b9c9b0f9c9a0001b0b1f5', '5e9b9c9b0f9c9a0001b0b1f6'].
    """

    name: str
    workspace_id: Union[Unset, str] = UNSET
    organisation_id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    participant_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        workspace_id = self.workspace_id
        organisation_id = self.organisation_id
        description = self.description
        participant_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.participant_ids, Unset):
            participant_ids = self.participant_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if organisation_id is not UNSET:
            field_dict["organisation_id"] = organisation_id
        if description is not UNSET:
            field_dict["description"] = description
        if participant_ids is not UNSET:
            field_dict["participant_ids"] = participant_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        workspace_id = d.pop("workspace_id", UNSET)

        organisation_id = d.pop("organisation_id", UNSET)

        description = d.pop("description", UNSET)

        participant_ids = cast(List[str], d.pop("participant_ids", UNSET))

        create_participant_group_json_body = cls(
            name=name,
            workspace_id=workspace_id,
            organisation_id=organisation_id,
            description=description,
            participant_ids=participant_ids,
        )

        create_participant_group_json_body.additional_properties = d
        return create_participant_group_json_body

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
