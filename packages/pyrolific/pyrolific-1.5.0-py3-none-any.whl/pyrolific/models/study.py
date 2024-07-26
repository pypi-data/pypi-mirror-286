from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.base_study_content_warnings_item import BaseStudyContentWarningsItem
from ..models.base_study_device_compatibility_item import BaseStudyDeviceCompatibilityItem
from ..models.base_study_peripheral_requirements_item import BaseStudyPeripheralRequirementsItem
from ..models.base_study_prolific_id_option import BaseStudyProlificIdOption
from ..models.base_study_study_labels_item import BaseStudyStudyLabelsItem
from ..models.study_status import StudyStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.access_detail import AccessDetail
    from ..models.base_study_completion_codes_item import BaseStudyCompletionCodesItem
    from ..models.base_study_submissions_config import BaseStudySubmissionsConfig
    from ..models.range_filter import RangeFilter
    from ..models.select_filter import SelectFilter


T = TypeVar("T", bound="Study")


@_attrs_define
class Study:
    r"""
    Example:
        {'id': '60d9aadeb86739de712faee0', 'name': "Study about API's", 'internal_name': "WIT-2021 Study about API's
            version 2", 'description': 'This study aims to determine how to make a good public API', 'external_study_url':
            'https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}', 'prolific_id_option': 'url_parameters',
            'completion_codes': [{'code': 'ABC123', 'code_type': 'COMPLETED', 'actions': [{'action':
            'AUTOMATICALLY_APPROVE'}]}, {'code': 'DEF234', 'code_type': 'FOLLOW_UP_STUDY', 'actions': [{'action':
            'AUTOMATICALLY_APPROVE'}, {'action': 'ADD_TO_PARTICIPANT_GROUP', 'participant_group':
            '619e049f7648a4e1f8f3645b'}]}], 'total_available_places': 30, 'estimated_completion_time': 5,
            'maximum_allowed_time': 25, 'reward': 100, 'device_compatibility': ['desktop'], 'peripheral_requirements': [],
            'filters': [], 'filter_set_id': None, 'filter_set_version': None, 'status': 'UNPUBLISHED', 'study_labels':
            ['interview'], 'content_warnings': ['sensitive'], 'content_warning_details': 'Experiences with hateful
            activities, experiences with self-injury and harmful behaviour'}

    Attributes:
        id (str): Study id. It is created by Prolific. **Read only**.
        status (StudyStatus): Status of the study. **Read only**.

            To change the status you can use `/api/v1/studies/{id}/transition/`
        name (Union[Unset, str]): Public name or title of the study
        internal_name (Union[None, Unset, str]): Internal name of the study, not shown to participants
        description (Union[Unset, str]): Description of the study for the participants to read before
            starting the study
        external_study_url (Union[Unset, str]): URL of the survey or experiment you want participant to access. You can
            pass URL search parameters to your survey or experiment

            * Participant id {{%PROLIFIC_PID%}}
            * Study id {{%STUDY_ID%}}
            * Session id {{%SESSION_ID%}}

            For example `https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}`
        prolific_id_option (Union[Unset, BaseStudyProlificIdOption]): Use 'question' if you will add a question in your
            survey or experiment asking the participant ID

            **Recommended** Use 'url_parameters' if your survey or experiment can retrieve and store those parameters for
            your analysis.

            Use 'not_required' if you don't need to record them
        completion_codes (Union[Unset, List['BaseStudyCompletionCodesItem']]): Specify at least one completion code for
            your study. A participant will enter one of these codes when they complete your study.

            Each code must be unique within a study.

            You can specify as many actions as you like per code.
        total_available_places (Union[Unset, float]): How many participants are you looking to recruit
        estimated_completion_time (Union[Unset, float]): Estimated duration in minutes of the experiment or survey
        maximum_allowed_time (Union[Unset, float]): Max time in minutes for a participant to finish the submission.
            Submissions are timed out if it takes longer.

            If it is not provided the default value is set to the max value.

            The min value is calculated as two minutes plus two times the estimated time plus two times the square root of
            the estimated time
        reward (Union[Unset, float]): How much are you going to pay the participants in cents. We
            use the currency of your account.
        device_compatibility (Union[Unset, List[BaseStudyDeviceCompatibilityItem]]): Add all devices that participants
            can use.
            You can include one or more options.

            An empty array indicates that all options are available.
        peripheral_requirements (Union[Unset, List[BaseStudyPeripheralRequirementsItem]]): Add all requirements that
            participants have to meet.

            An empty array indicates that there are no extra peripheral requirements.
        filters (Union[List[Union['RangeFilter', 'SelectFilter']], None, Unset]): Array of filters.

            Use empty array for "Everyone"
        filter_set_id (Union[None, Unset, str]): The ID of a filter set, from which filters for the study will be taken.

            Note, this cannot be used in combination with additional filters via the `filters` field.
        filter_set_version (Union[None, Unset, int]): The version of the filter set to be used.

            If not provided, this will default to the latest available version at the time of applying the filter set.
        naivety_distribution_rate (Union[None, Unset, float]): Control the balance between speed of your studies and the
            naivety of the participants.

            If not defined, by default Prolific calculates the best rate for most studies
            taking into account the `filters` and the `total_available_places` needed for this study.

            Use 0 if your priority is speed. When this property is set to 0 all eligible participants will have access
            to your study at the same time, without any prioritization.

            You can also set this at a workspace and project level.
        project (Union[Unset, str]): Project id, this is optional and if not supplied with be the put in the default
            workspace and project.
        submissions_config (Union[Unset, BaseStudySubmissionsConfig]): **Advanced**: This helps with faster data
            collection. Your survey system will need to handle providing a
            unique experience each time the participant takes the study.

            Configuration related to study submissions. The purpose of this field is to capture any configuration options
            that impact the submissions made by participants in a study.
        study_labels (Union[Unset, List[BaseStudyStudyLabelsItem]]): This field allows you to tag studies with
            information about the type/topic of the study and the kind of work involved in completing it.

            We plan to make this information available to participants for easier self-selection. At present these options
            are mutually exclusive and only a single option can be selected, however in the future available categories will
            expand.
        content_warnings (Union[Unset, List[BaseStudyContentWarningsItem]]): Allow researchers to define content
            warnings for their study.

            At present these options are mutually exclusive and only a single option can be selected, however in the future
            available warnings will expand.
        content_warning_details (Union[Unset, str]): Allow researchers to add further details about their content
            warning.
        metadata (Union[None, Unset, str]): This field can be used to store extra information required for a system
            integration.
            For example, it could be some JSON, XML, an integer, or a string.

            Examples could include:

              - `123345` - An ID from your system, that helps with linkage when returning the study.
              - `{ \"id\": \"45\", \"type\": \"finance\"}` - Some JSON that you want to store.
        access_details (Union[List['AccessDetail'], None, Unset]): Array of access_details, which integrates with
            taskflow.

            While this field is nullable, you must provide one of `access_details` or `external_study_url`.

            The sum of all access_details must add to the `total_available_places` field, however the values can be
            different for an individual access_detail.
    """

    id: str
    status: StudyStatus
    name: Union[Unset, str] = UNSET
    internal_name: Union[None, Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    external_study_url: Union[Unset, str] = UNSET
    prolific_id_option: Union[Unset, BaseStudyProlificIdOption] = UNSET
    completion_codes: Union[Unset, List["BaseStudyCompletionCodesItem"]] = UNSET
    total_available_places: Union[Unset, float] = UNSET
    estimated_completion_time: Union[Unset, float] = UNSET
    maximum_allowed_time: Union[Unset, float] = UNSET
    reward: Union[Unset, float] = UNSET
    device_compatibility: Union[Unset, List[BaseStudyDeviceCompatibilityItem]] = UNSET
    peripheral_requirements: Union[Unset, List[BaseStudyPeripheralRequirementsItem]] = UNSET
    filters: Union[List[Union["RangeFilter", "SelectFilter"]], None, Unset] = UNSET
    filter_set_id: Union[None, Unset, str] = UNSET
    filter_set_version: Union[None, Unset, int] = UNSET
    naivety_distribution_rate: Union[None, Unset, float] = UNSET
    project: Union[Unset, str] = UNSET
    submissions_config: Union[Unset, "BaseStudySubmissionsConfig"] = UNSET
    study_labels: Union[Unset, List[BaseStudyStudyLabelsItem]] = UNSET
    content_warnings: Union[Unset, List[BaseStudyContentWarningsItem]] = UNSET
    content_warning_details: Union[Unset, str] = UNSET
    metadata: Union[None, Unset, str] = UNSET
    access_details: Union[List["AccessDetail"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.select_filter import SelectFilter

        id = self.id

        status = self.status.value

        name = self.name

        internal_name: Union[None, Unset, str]
        if isinstance(self.internal_name, Unset):
            internal_name = UNSET
        else:
            internal_name = self.internal_name

        description = self.description

        external_study_url = self.external_study_url

        prolific_id_option: Union[Unset, str] = UNSET
        if not isinstance(self.prolific_id_option, Unset):
            prolific_id_option = self.prolific_id_option.value

        completion_codes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.completion_codes, Unset):
            completion_codes = []
            for completion_codes_item_data in self.completion_codes:
                completion_codes_item = completion_codes_item_data.to_dict()
                completion_codes.append(completion_codes_item)

        total_available_places = self.total_available_places

        estimated_completion_time = self.estimated_completion_time

        maximum_allowed_time = self.maximum_allowed_time

        reward = self.reward

        device_compatibility: Union[Unset, List[str]] = UNSET
        if not isinstance(self.device_compatibility, Unset):
            device_compatibility = []
            for device_compatibility_item_data in self.device_compatibility:
                device_compatibility_item = device_compatibility_item_data.value
                device_compatibility.append(device_compatibility_item)

        peripheral_requirements: Union[Unset, List[str]] = UNSET
        if not isinstance(self.peripheral_requirements, Unset):
            peripheral_requirements = []
            for peripheral_requirements_item_data in self.peripheral_requirements:
                peripheral_requirements_item = peripheral_requirements_item_data.value
                peripheral_requirements.append(peripheral_requirements_item)

        filters: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.filters, Unset):
            filters = UNSET
        elif isinstance(self.filters, list):
            filters = []
            for filters_type_0_item_data in self.filters:
                filters_type_0_item: Dict[str, Any]
                if isinstance(filters_type_0_item_data, SelectFilter):
                    filters_type_0_item = filters_type_0_item_data.to_dict()
                else:
                    filters_type_0_item = filters_type_0_item_data.to_dict()

                filters.append(filters_type_0_item)

        else:
            filters = self.filters

        filter_set_id: Union[None, Unset, str]
        if isinstance(self.filter_set_id, Unset):
            filter_set_id = UNSET
        else:
            filter_set_id = self.filter_set_id

        filter_set_version: Union[None, Unset, int]
        if isinstance(self.filter_set_version, Unset):
            filter_set_version = UNSET
        else:
            filter_set_version = self.filter_set_version

        naivety_distribution_rate: Union[None, Unset, float]
        if isinstance(self.naivety_distribution_rate, Unset):
            naivety_distribution_rate = UNSET
        else:
            naivety_distribution_rate = self.naivety_distribution_rate

        project = self.project

        submissions_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.submissions_config, Unset):
            submissions_config = self.submissions_config.to_dict()

        study_labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.study_labels, Unset):
            study_labels = []
            for study_labels_item_data in self.study_labels:
                study_labels_item = study_labels_item_data.value
                study_labels.append(study_labels_item)

        content_warnings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.content_warnings, Unset):
            content_warnings = []
            for content_warnings_item_data in self.content_warnings:
                content_warnings_item = content_warnings_item_data.value
                content_warnings.append(content_warnings_item)

        content_warning_details = self.content_warning_details

        metadata: Union[None, Unset, str]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        else:
            metadata = self.metadata

        access_details: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.access_details, Unset):
            access_details = UNSET
        elif isinstance(self.access_details, list):
            access_details = []
            for access_details_type_0_item_data in self.access_details:
                access_details_type_0_item = access_details_type_0_item_data.to_dict()
                access_details.append(access_details_type_0_item)

        else:
            access_details = self.access_details

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if internal_name is not UNSET:
            field_dict["internal_name"] = internal_name
        if description is not UNSET:
            field_dict["description"] = description
        if external_study_url is not UNSET:
            field_dict["external_study_url"] = external_study_url
        if prolific_id_option is not UNSET:
            field_dict["prolific_id_option"] = prolific_id_option
        if completion_codes is not UNSET:
            field_dict["completion_codes"] = completion_codes
        if total_available_places is not UNSET:
            field_dict["total_available_places"] = total_available_places
        if estimated_completion_time is not UNSET:
            field_dict["estimated_completion_time"] = estimated_completion_time
        if maximum_allowed_time is not UNSET:
            field_dict["maximum_allowed_time"] = maximum_allowed_time
        if reward is not UNSET:
            field_dict["reward"] = reward
        if device_compatibility is not UNSET:
            field_dict["device_compatibility"] = device_compatibility
        if peripheral_requirements is not UNSET:
            field_dict["peripheral_requirements"] = peripheral_requirements
        if filters is not UNSET:
            field_dict["filters"] = filters
        if filter_set_id is not UNSET:
            field_dict["filter_set_id"] = filter_set_id
        if filter_set_version is not UNSET:
            field_dict["filter_set_version"] = filter_set_version
        if naivety_distribution_rate is not UNSET:
            field_dict["naivety_distribution_rate"] = naivety_distribution_rate
        if project is not UNSET:
            field_dict["project"] = project
        if submissions_config is not UNSET:
            field_dict["submissions_config"] = submissions_config
        if study_labels is not UNSET:
            field_dict["study_labels"] = study_labels
        if content_warnings is not UNSET:
            field_dict["content_warnings"] = content_warnings
        if content_warning_details is not UNSET:
            field_dict["content_warning_details"] = content_warning_details
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if access_details is not UNSET:
            field_dict["access_details"] = access_details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.access_detail import AccessDetail
        from ..models.base_study_completion_codes_item import BaseStudyCompletionCodesItem
        from ..models.base_study_submissions_config import BaseStudySubmissionsConfig
        from ..models.range_filter import RangeFilter
        from ..models.select_filter import SelectFilter

        d = src_dict.copy()
        id = d.pop("id")

        status = StudyStatus(d.pop("status"))

        name = d.pop("name", UNSET)

        def _parse_internal_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        internal_name = _parse_internal_name(d.pop("internal_name", UNSET))

        description = d.pop("description", UNSET)

        external_study_url = d.pop("external_study_url", UNSET)

        _prolific_id_option = d.pop("prolific_id_option", UNSET)
        prolific_id_option: Union[Unset, BaseStudyProlificIdOption]
        if isinstance(_prolific_id_option, Unset):
            prolific_id_option = UNSET
        else:
            prolific_id_option = BaseStudyProlificIdOption(_prolific_id_option)

        completion_codes = []
        _completion_codes = d.pop("completion_codes", UNSET)
        for completion_codes_item_data in _completion_codes or []:
            completion_codes_item = BaseStudyCompletionCodesItem.from_dict(completion_codes_item_data)

            completion_codes.append(completion_codes_item)

        total_available_places = d.pop("total_available_places", UNSET)

        estimated_completion_time = d.pop("estimated_completion_time", UNSET)

        maximum_allowed_time = d.pop("maximum_allowed_time", UNSET)

        reward = d.pop("reward", UNSET)

        device_compatibility = []
        _device_compatibility = d.pop("device_compatibility", UNSET)
        for device_compatibility_item_data in _device_compatibility or []:
            device_compatibility_item = BaseStudyDeviceCompatibilityItem(device_compatibility_item_data)

            device_compatibility.append(device_compatibility_item)

        peripheral_requirements = []
        _peripheral_requirements = d.pop("peripheral_requirements", UNSET)
        for peripheral_requirements_item_data in _peripheral_requirements or []:
            peripheral_requirements_item = BaseStudyPeripheralRequirementsItem(peripheral_requirements_item_data)

            peripheral_requirements.append(peripheral_requirements_item)

        def _parse_filters(data: object) -> Union[List[Union["RangeFilter", "SelectFilter"]], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filters_type_0 = []
                _filters_type_0 = data
                for filters_type_0_item_data in _filters_type_0:

                    def _parse_filters_type_0_item(data: object) -> Union["RangeFilter", "SelectFilter"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            filters_type_0_item_type_0 = SelectFilter.from_dict(data)

                            return filters_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_type_0_item_type_1 = RangeFilter.from_dict(data)

                        return filters_type_0_item_type_1

                    filters_type_0_item = _parse_filters_type_0_item(filters_type_0_item_data)

                    filters_type_0.append(filters_type_0_item)

                return filters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[Union["RangeFilter", "SelectFilter"]], None, Unset], data)

        filters = _parse_filters(d.pop("filters", UNSET))

        def _parse_filter_set_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        filter_set_id = _parse_filter_set_id(d.pop("filter_set_id", UNSET))

        def _parse_filter_set_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        filter_set_version = _parse_filter_set_version(d.pop("filter_set_version", UNSET))

        def _parse_naivety_distribution_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        naivety_distribution_rate = _parse_naivety_distribution_rate(d.pop("naivety_distribution_rate", UNSET))

        project = d.pop("project", UNSET)

        _submissions_config = d.pop("submissions_config", UNSET)
        submissions_config: Union[Unset, BaseStudySubmissionsConfig]
        if isinstance(_submissions_config, Unset):
            submissions_config = UNSET
        else:
            submissions_config = BaseStudySubmissionsConfig.from_dict(_submissions_config)

        study_labels = []
        _study_labels = d.pop("study_labels", UNSET)
        for study_labels_item_data in _study_labels or []:
            study_labels_item = BaseStudyStudyLabelsItem(study_labels_item_data)

            study_labels.append(study_labels_item)

        content_warnings = []
        _content_warnings = d.pop("content_warnings", UNSET)
        for content_warnings_item_data in _content_warnings or []:
            content_warnings_item = BaseStudyContentWarningsItem(content_warnings_item_data)

            content_warnings.append(content_warnings_item)

        content_warning_details = d.pop("content_warning_details", UNSET)

        def _parse_metadata(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_access_details(data: object) -> Union[List["AccessDetail"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                access_details_type_0 = []
                _access_details_type_0 = data
                for access_details_type_0_item_data in _access_details_type_0:
                    access_details_type_0_item = AccessDetail.from_dict(access_details_type_0_item_data)

                    access_details_type_0.append(access_details_type_0_item)

                return access_details_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["AccessDetail"], None, Unset], data)

        access_details = _parse_access_details(d.pop("access_details", UNSET))

        study = cls(
            id=id,
            status=status,
            name=name,
            internal_name=internal_name,
            description=description,
            external_study_url=external_study_url,
            prolific_id_option=prolific_id_option,
            completion_codes=completion_codes,
            total_available_places=total_available_places,
            estimated_completion_time=estimated_completion_time,
            maximum_allowed_time=maximum_allowed_time,
            reward=reward,
            device_compatibility=device_compatibility,
            peripheral_requirements=peripheral_requirements,
            filters=filters,
            filter_set_id=filter_set_id,
            filter_set_version=filter_set_version,
            naivety_distribution_rate=naivety_distribution_rate,
            project=project,
            submissions_config=submissions_config,
            study_labels=study_labels,
            content_warnings=content_warnings,
            content_warning_details=content_warning_details,
            metadata=metadata,
            access_details=access_details,
        )

        study.additional_properties = d
        return study

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
