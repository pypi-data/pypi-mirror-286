from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.summary import Summary
from ...types import Response


def _get_kwargs(
    survey_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/surveys/{survey_id}/responses/summary/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Summary]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Summary.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Summary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Summary]:
    """Get summary of responses

     Get an aggregated summary of responses for a given survey.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Summary]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Summary]:
    """Get summary of responses

     Get an aggregated summary of responses for a given survey.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Summary
    """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Summary]:
    """Get summary of responses

     Get an aggregated summary of responses for a given survey.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Summary]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Summary]:
    """Get summary of responses

     Get an aggregated summary of responses for a given survey.

    Args:
        survey_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Summary
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
        )
    ).parsed
