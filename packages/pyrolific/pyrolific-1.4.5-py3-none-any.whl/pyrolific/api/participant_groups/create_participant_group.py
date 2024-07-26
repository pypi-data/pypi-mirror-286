from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.participant_group import ParticipantGroup
from ...models.create_participant_group_json_body import CreateParticipantGroupJsonBody
from typing import Dict


def _get_kwargs(
    *,
    json_body: CreateParticipantGroupJsonBody,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/participant-groups/",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ParticipantGroup]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ParticipantGroup.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ParticipantGroup]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateParticipantGroupJsonBody,
) -> Response[ParticipantGroup]:
    """Create a new participant group within a workspace

    Args:
        json_body (CreateParticipantGroupJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroup]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: CreateParticipantGroupJsonBody,
) -> Optional[ParticipantGroup]:
    """Create a new participant group within a workspace

    Args:
        json_body (CreateParticipantGroupJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroup
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateParticipantGroupJsonBody,
) -> Response[ParticipantGroup]:
    """Create a new participant group within a workspace

    Args:
        json_body (CreateParticipantGroupJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroup]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: CreateParticipantGroupJsonBody,
) -> Optional[ParticipantGroup]:
    """Create a new participant group within a workspace

    Args:
        json_body (CreateParticipantGroupJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroup
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
