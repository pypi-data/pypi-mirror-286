from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.messages import Messages
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    user_id: Union[Unset, str] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}

    params["user_id"] = user_id

    params["created_after"] = created_after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/messages/",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Messages]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Messages.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Messages]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, str] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    authorization: str,
) -> Response[Messages]:
    """Retrieve messages

     Get messages between you and another user or your messages with all users.

    Args:
        user_id (Union[Unset, str]):
        created_after (Union[Unset, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Messages]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        created_after=created_after,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, str] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    authorization: str,
) -> Optional[Messages]:
    """Retrieve messages

     Get messages between you and another user or your messages with all users.

    Args:
        user_id (Union[Unset, str]):
        created_after (Union[Unset, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Messages
    """

    return sync_detailed(
        client=client,
        user_id=user_id,
        created_after=created_after,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, str] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    authorization: str,
) -> Response[Messages]:
    """Retrieve messages

     Get messages between you and another user or your messages with all users.

    Args:
        user_id (Union[Unset, str]):
        created_after (Union[Unset, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Messages]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        created_after=created_after,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    user_id: Union[Unset, str] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    authorization: str,
) -> Optional[Messages]:
    """Retrieve messages

     Get messages between you and another user or your messages with all users.

    Args:
        user_id (Union[Unset, str]):
        created_after (Union[Unset, str]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Messages
    """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
            created_after=created_after,
            authorization=authorization,
        )
    ).parsed
