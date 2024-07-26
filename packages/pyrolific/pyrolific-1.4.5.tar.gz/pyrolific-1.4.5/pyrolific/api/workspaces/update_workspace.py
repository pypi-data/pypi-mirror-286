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
    json_body: Workspace,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": "/api/v1/workspaces/{workspace_id}/".format(
            workspace_id=workspace_id,
        ),
        "json": json_json_body,
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
    json_body: Workspace,
    authorization: str,
) -> Response[Workspace]:
    """Update a workspace

     Updates a workspace's details.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (Workspace):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My
            workspace', 'description': 'This workspace does...', 'owner': '60a42f4c693c29420793cb73',
            'users': [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email':
            'joe.soap@gmail.com', 'roles': ['WORKSPACE_ADMIN']}], 'projects': [{'id':
            '60a42f4c693c29420793cb73'}], 'wallet': '61a65c06b084910b3f0c00d6'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        json_body=json_body,
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
    json_body: Workspace,
    authorization: str,
) -> Optional[Workspace]:
    """Update a workspace

     Updates a workspace's details.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (Workspace):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My
            workspace', 'description': 'This workspace does...', 'owner': '60a42f4c693c29420793cb73',
            'users': [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email':
            'joe.soap@gmail.com', 'roles': ['WORKSPACE_ADMIN']}], 'projects': [{'id':
            '60a42f4c693c29420793cb73'}], 'wallet': '61a65c06b084910b3f0c00d6'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Workspace
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    authorization: str,
) -> Response[Workspace]:
    """Update a workspace

     Updates a workspace's details.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (Workspace):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My
            workspace', 'description': 'This workspace does...', 'owner': '60a42f4c693c29420793cb73',
            'users': [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email':
            'joe.soap@gmail.com', 'roles': ['WORKSPACE_ADMIN']}], 'projects': [{'id':
            '60a42f4c693c29420793cb73'}], 'wallet': '61a65c06b084910b3f0c00d6'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workspace]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        json_body=json_body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    authorization: str,
) -> Optional[Workspace]:
    """Update a workspace

     Updates a workspace's details.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (Workspace):  Example: {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My
            workspace', 'description': 'This workspace does...', 'owner': '60a42f4c693c29420793cb73',
            'users': [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email':
            'joe.soap@gmail.com', 'roles': ['WORKSPACE_ADMIN']}], 'projects': [{'id':
            '60a42f4c693c29420793cb73'}], 'wallet': '61a65c06b084910b3f0c00d6'}.

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
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
