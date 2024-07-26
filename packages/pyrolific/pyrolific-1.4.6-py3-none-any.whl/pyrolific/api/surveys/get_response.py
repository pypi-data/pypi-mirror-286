from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.response_out import ResponseOut
from typing import Dict


def _get_kwargs(
    survey_id: str,
    response_id: str,
) -> Dict[str, Any]:
    return {
        "method": "get",
        "url": "/api/v1/surveys/{survey_id}/responses/{response_id}".format(
            survey_id=survey_id,
            response_id=response_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResponseOut]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ResponseOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResponseOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ResponseOut]:
    """Get response

     Get a single response for a survey.

    Args:
        survey_id (str):
        response_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseOut]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        response_id=response_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseOut]:
    """Get response

     Get a single response for a survey.

    Args:
        survey_id (str):
        response_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseOut
    """

    return sync_detailed(
        survey_id=survey_id,
        response_id=response_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ResponseOut]:
    """Get response

     Get a single response for a survey.

    Args:
        survey_id (str):
        response_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseOut]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        response_id=response_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    response_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseOut]:
    """Get response

     Get a single response for a survey.

    Args:
        survey_id (str):
        response_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseOut
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            response_id=response_id,
            client=client,
        )
    ).parsed
