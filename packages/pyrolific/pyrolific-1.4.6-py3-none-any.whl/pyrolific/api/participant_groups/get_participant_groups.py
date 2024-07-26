from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from typing import Union
from ...models.project_id import ProjectID
from typing import Union
from ...models.get_participant_groups_active import GetParticipantGroupsActive
from typing import Optional
from ...models.workspace_id import WorkspaceID
from typing import Dict
from ...models.participant_group_list_response import ParticipantGroupListResponse


def _get_kwargs(
    *,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    filter_: Union["ProjectID", "WorkspaceID"],
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    json_active: Union[Unset, None, str] = UNSET
    if not isinstance(active, Unset):
        json_active = active.value if active else None

    params["active"] = json_active

    json_filter_: Dict[str, Any]

    if isinstance(filter_, WorkspaceID):
        json_filter_ = filter_.to_dict()

    else:
        json_filter_ = filter_.to_dict()

    params["filter"] = json_filter_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v1/participant-groups/",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ParticipantGroupListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ParticipantGroupListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ParticipantGroupListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    filter_: Union["ProjectID", "WorkspaceID"],
) -> Response[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project or workspace

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        filter_ (Union['ProjectID', 'WorkspaceID']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupListResponse]
    """

    kwargs = _get_kwargs(
        active=active,
        filter_=filter_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    filter_: Union["ProjectID", "WorkspaceID"],
) -> Optional[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project or workspace

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        filter_ (Union['ProjectID', 'WorkspaceID']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupListResponse
    """

    return sync_detailed(
        client=client,
        active=active,
        filter_=filter_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    filter_: Union["ProjectID", "WorkspaceID"],
) -> Response[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project or workspace

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        filter_ (Union['ProjectID', 'WorkspaceID']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ParticipantGroupListResponse]
    """

    kwargs = _get_kwargs(
        active=active,
        filter_=filter_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    active: Union[Unset, None, GetParticipantGroupsActive] = UNSET,
    filter_: Union["ProjectID", "WorkspaceID"],
) -> Optional[ParticipantGroupListResponse]:
    """Get a list of all participant groups within a project or workspace

    Args:
        active (Union[Unset, None, GetParticipantGroupsActive]):
        filter_ (Union['ProjectID', 'WorkspaceID']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ParticipantGroupListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            active=active,
            filter_=filter_,
        )
    ).parsed
