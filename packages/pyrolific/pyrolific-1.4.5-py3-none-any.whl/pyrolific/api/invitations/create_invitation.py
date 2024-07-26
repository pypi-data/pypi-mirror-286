from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.create_invitation_request import CreateInvitationRequest
from typing import Dict
from ...models.create_invitation_response import CreateInvitationResponse


def _get_kwargs(
    *,
    json_body: CreateInvitationRequest,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/invitations/",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CreateInvitationResponse]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateInvitationResponse.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateInvitationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateInvitationRequest,
    authorization: str,
) -> Response[CreateInvitationResponse]:
    """Create a new invitation

     Initiate a new invitation process for adding users to a Workspace or Project.

    This operation can be performed only by authenticated users who are admins for the specified
    workspace. Invitations will be sent to the email addresses provided in the request.

    Args:
        authorization (str):
        json_body (CreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateInvitationResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: CreateInvitationRequest,
    authorization: str,
) -> Optional[CreateInvitationResponse]:
    """Create a new invitation

     Initiate a new invitation process for adding users to a Workspace or Project.

    This operation can be performed only by authenticated users who are admins for the specified
    workspace. Invitations will be sent to the email addresses provided in the request.

    Args:
        authorization (str):
        json_body (CreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateInvitationResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateInvitationRequest,
    authorization: str,
) -> Response[CreateInvitationResponse]:
    """Create a new invitation

     Initiate a new invitation process for adding users to a Workspace or Project.

    This operation can be performed only by authenticated users who are admins for the specified
    workspace. Invitations will be sent to the email addresses provided in the request.

    Args:
        authorization (str):
        json_body (CreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateInvitationResponse]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: CreateInvitationRequest,
    authorization: str,
) -> Optional[CreateInvitationResponse]:
    """Create a new invitation

     Initiate a new invitation process for adding users to a Workspace or Project.

    This operation can be performed only by authenticated users who are admins for the specified
    workspace. Invitations will be sent to the email addresses provided in the request.

    Args:
        authorization (str):
        json_body (CreateInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateInvitationResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
