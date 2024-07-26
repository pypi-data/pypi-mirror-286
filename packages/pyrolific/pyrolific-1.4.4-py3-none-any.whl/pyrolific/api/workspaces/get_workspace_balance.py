from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.workspace_balance import WorkspaceBalance
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
        "url": "/api/v1/workspaces/{workspace_id}/balance/".format(
            workspace_id=workspace_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[WorkspaceBalance]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceBalance.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WorkspaceBalance]:
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
) -> Response[WorkspaceBalance]:
    """Get the balance of a workspace

     Provides details of the funds available in the workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceBalance]
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
) -> Optional[WorkspaceBalance]:
    """Get the balance of a workspace

     Provides details of the funds available in the workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceBalance
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
) -> Response[WorkspaceBalance]:
    """Get the balance of a workspace

     Provides details of the funds available in the workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceBalance]
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
) -> Optional[WorkspaceBalance]:
    """Get the balance of a workspace

     Provides details of the funds available in the workspace.

    Args:
        workspace_id (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceBalance
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            authorization=authorization,
        )
    ).parsed
