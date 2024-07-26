import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.submission_short_status import SubmissionShortStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmissionShort")


@_attrs_define
class SubmissionShort:
    """
    Example:
        {'id': '60d9aadeb86739de712faee0', 'participant_id': '60bf9310e8dec401be6e9615', 'started_at':
            datetime.datetime(2021, 5, 20, 11, 3, 0, 457000, tzinfo=datetime.timezone(datetime.timedelta(0), 'Z')),
            'status': 'ACTIVE', 'study_code': 'ABC123'}

    Attributes:
        id (str): Submission id.
        participant_id (str): Participant id.
        status (SubmissionShortStatus): Status of the submission.
        started_at (datetime.datetime): Date started
        has_siblings (bool): Whether or not the submission has sibling submissions (sharing the same study).
        completed_at (Union[None, Unset, datetime.datetime]): Date completed
        study_code (Union[None, Unset, str]): The completion code used by the participant to complete the study.
    """

    id: str
    participant_id: str
    status: SubmissionShortStatus
    started_at: datetime.datetime
    has_siblings: bool
    completed_at: Union[None, Unset, datetime.datetime] = UNSET
    study_code: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        participant_id = self.participant_id

        status = self.status.value

        started_at = self.started_at.isoformat()

        has_siblings = self.has_siblings

        completed_at: Union[None, Unset, str]
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        study_code: Union[None, Unset, str]
        if isinstance(self.study_code, Unset):
            study_code = UNSET
        else:
            study_code = self.study_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "participant_id": participant_id,
                "status": status,
                "started_at": started_at,
                "has_siblings": has_siblings,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if study_code is not UNSET:
            field_dict["study_code"] = study_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        participant_id = d.pop("participant_id")

        status = SubmissionShortStatus(d.pop("status"))

        started_at = isoparse(d.pop("started_at"))

        has_siblings = d.pop("has_siblings")

        def _parse_completed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        def _parse_study_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        study_code = _parse_study_code(d.pop("study_code", UNSET))

        submission_short = cls(
            id=id,
            participant_id=participant_id,
            status=status,
            started_at=started_at,
            has_siblings=has_siblings,
            completed_at=completed_at,
            study_code=study_code,
        )

        submission_short.additional_properties = d
        return submission_short

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
