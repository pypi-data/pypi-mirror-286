from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.submission_list_response import SubmissionListResponse
from ...types import UNSET, Unset
from typing import Union
from typing import Optional
from typing import Dict


def _get_kwargs(
    *,
    study: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}
    params["study"] = study

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v1/submissions/",
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SubmissionListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SubmissionListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SubmissionListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    study: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Response[SubmissionListResponse]:
    """List submissions

     Returns basic information of the submissions, including the study id, participant id, status and
    start timestamp

    Args:
        study (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubmissionListResponse]
    """

    kwargs = _get_kwargs(
        study=study,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    study: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Optional[SubmissionListResponse]:
    """List submissions

     Returns basic information of the submissions, including the study id, participant id, status and
    start timestamp

    Args:
        study (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubmissionListResponse
    """

    return sync_detailed(
        client=client,
        study=study,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    study: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Response[SubmissionListResponse]:
    """List submissions

     Returns basic information of the submissions, including the study id, participant id, status and
    start timestamp

    Args:
        study (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubmissionListResponse]
    """

    kwargs = _get_kwargs(
        study=study,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    study: Union[Unset, None, str] = UNSET,
    authorization: str,
) -> Optional[SubmissionListResponse]:
    """List submissions

     Returns basic information of the submissions, including the study id, participant id, status and
    start timestamp

    Args:
        study (Union[Unset, None, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubmissionListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            study=study,
            authorization=authorization,
        )
    ).parsed
