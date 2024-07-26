from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.question_response import QuestionResponse


T = TypeVar("T", bound="Section")


@_attrs_define
class Section:
    """Responsible for linking question/answers to a response for a survey.

    This is more of a long term thing, but helps if we add now.

        Attributes:
            questions (List['QuestionResponse']): The questions for a given section.
            section_id (str): The section ID.
    """

    questions: List["QuestionResponse"]
    section_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        section_id = self.section_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "questions": questions,
                "section_id": section_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.question_response import QuestionResponse

        d = src_dict.copy()
        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = QuestionResponse.from_dict(questions_item_data)

            questions.append(questions_item)

        section_id = d.pop("section_id")

        section = cls(
            questions=questions,
            section_id=section_id,
        )

        section.additional_properties = d
        return section

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
