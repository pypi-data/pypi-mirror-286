from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.study_predicted_recruitment_time import StudyPredictedRecruitmentTime
from ...types import Response


def _get_kwargs(
    study_id: str,
    *,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/studies/{study_id}/predicted-recruitment-time/",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[StudyPredictedRecruitmentTime]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StudyPredictedRecruitmentTime.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[StudyPredictedRecruitmentTime]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    study_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[StudyPredictedRecruitmentTime]:
    """Show Study predicted reqruitment time

     Returns the predicted recruitment time for the study if it was published right now, based on a
    machine learning model.
    The recruitment time is the time from publish to the time when the final participant starts their
    submission.
    It does not account for the time to complete the submission.

    Args:
        study_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudyPredictedRecruitmentTime]
    """

    kwargs = _get_kwargs(
        study_id=study_id,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    study_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[StudyPredictedRecruitmentTime]:
    """Show Study predicted reqruitment time

     Returns the predicted recruitment time for the study if it was published right now, based on a
    machine learning model.
    The recruitment time is the time from publish to the time when the final participant starts their
    submission.
    It does not account for the time to complete the submission.

    Args:
        study_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudyPredictedRecruitmentTime
    """

    return sync_detailed(
        study_id=study_id,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    study_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[StudyPredictedRecruitmentTime]:
    """Show Study predicted reqruitment time

     Returns the predicted recruitment time for the study if it was published right now, based on a
    machine learning model.
    The recruitment time is the time from publish to the time when the final participant starts their
    submission.
    It does not account for the time to complete the submission.

    Args:
        study_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudyPredictedRecruitmentTime]
    """

    kwargs = _get_kwargs(
        study_id=study_id,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    study_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[StudyPredictedRecruitmentTime]:
    """Show Study predicted reqruitment time

     Returns the predicted recruitment time for the study if it was published right now, based on a
    machine learning model.
    The recruitment time is the time from publish to the time when the final participant starts their
    submission.
    It does not account for the time to complete the submission.

    Args:
        study_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudyPredictedRecruitmentTime
    """

    return (
        await asyncio_detailed(
            study_id=study_id,
            client=client,
            authorization=authorization,
        )
    ).parsed
