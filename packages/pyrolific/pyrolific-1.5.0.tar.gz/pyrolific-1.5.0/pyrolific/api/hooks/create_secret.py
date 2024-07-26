from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_secret import CreateSecret
from ...models.secret_detail import SecretDetail
from ...types import Response


def _get_kwargs(
    *,
    body: CreateSecret,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/hooks/secrets/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SecretDetail]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = SecretDetail.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SecretDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateSecret,
    authorization: str,
) -> Response[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SecretDetail]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateSecret,
    authorization: str,
) -> Optional[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SecretDetail
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateSecret,
    authorization: str,
) -> Response[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SecretDetail]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateSecret,
    authorization: str,
) -> Optional[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SecretDetail
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
