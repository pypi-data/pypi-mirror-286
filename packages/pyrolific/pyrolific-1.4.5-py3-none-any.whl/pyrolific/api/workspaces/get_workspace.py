from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.workspace import Workspace
from typing import Dict


def _get_kwargs(
    workspace_id: str,
    *,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    return {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/".format(
            workspace_id=workspace_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Workspace]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Workspace.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Workspace]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[Workspace]:
    """Get workspace

     Gets a workspace's details

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[Workspace]:
    """Get workspace

     Gets a workspace's details

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Workspace
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Response[Workspace]:
    """Get workspace

     Gets a workspace's details

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    authorization: str,
) -> Optional[Workspace]:
    """Get workspace

     Gets a workspace's details

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Workspace
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            authorization=authorization,
        )
    ).parsed
