from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.participant_group_membership_list_response import ParticipantGroupMembershipListResponse
from ...models.participant_id_list import ParticipantIDList
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: ParticipantIDList,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/api/v1/participant-groups/{id}/participants/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ParticipantGroupMembershipListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ParticipantGroupMembershipListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ParticipantGroupMembershipListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: ParticipantIDList,
) -> Response[ParticipantGroupMembershipListResponse]:
    """Remove participants from a participant group

     Remove specified participants from a participant group if they are members. If a participant is not
    a member of the group, they will be ignored.

    Args:
        id (str):
        body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupMembershipListResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: ParticipantIDList,
) -> Optional[ParticipantGroupMembershipListResponse]:
    """Remove participants from a participant group

     Remove specified participants from a participant group if they are members. If a participant is not
    a member of the group, they will be ignored.

    Args:
        id (str):
        body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupMembershipListResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: ParticipantIDList,
) -> Response[ParticipantGroupMembershipListResponse]:
    """Remove participants from a participant group

     Remove specified participants from a participant group if they are members. If a participant is not
    a member of the group, they will be ignored.

    Args:
        id (str):
        body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupMembershipListResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: ParticipantIDList,
) -> Optional[ParticipantGroupMembershipListResponse]:
    """Remove participants from a participant group

     Remove specified participants from a participant group if they are members. If a participant is not
    a member of the group, they will be ignored.

    Args:
        id (str):
        body (ParticipantIDList):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupMembershipListResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
