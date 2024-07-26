from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.create_project import CreateProject
from ...models.project import Project
from typing import Dict


def _get_kwargs(
    workspace_id: str,
    *,
    json_body: CreateProject,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/projects/".format(
            workspace_id=workspace_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Project]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Project.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Project]:
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
    json_body: CreateProject,
    authorization: str,
) -> Response[Project]:
    """Create a project

     Creates a new project within the workspace.
    When this project is created, it adds the user as a Project Editor.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (CreateProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Project]
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
    json_body: CreateProject,
    authorization: str,
) -> Optional[Project]:
    """Create a project

     Creates a new project within the workspace.
    When this project is created, it adds the user as a Project Editor.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (CreateProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Project
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
    json_body: CreateProject,
    authorization: str,
) -> Response[Project]:
    """Create a project

     Creates a new project within the workspace.
    When this project is created, it adds the user as a Project Editor.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (CreateProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Project]
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
    json_body: CreateProject,
    authorization: str,
) -> Optional[Project]:
    """Create a project

     Creates a new project within the workspace.
    When this project is created, it adds the user as a Project Editor.

    Args:
        workspace_id (str):
        authorization (str):
        json_body (CreateProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Project
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
