from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.secret_detail import SecretDetail
from typing import Dict
from ...models.create_secret import CreateSecret


def _get_kwargs(
    *,
    json_body: CreateSecret,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/hooks/secrets/",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SecretDetail]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = SecretDetail.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SecretDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateSecret,
    authorization: str,
) -> Response[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        json_body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SecretDetail]
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
    json_body: CreateSecret,
    authorization: str,
) -> Optional[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        json_body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SecretDetail
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateSecret,
    authorization: str,
) -> Response[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        json_body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SecretDetail]
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
    json_body: CreateSecret,
    authorization: str,
) -> Optional[SecretDetail]:
    """Create/replace a secret

     Generate a secret for verifying the request signature header of the subscription payload. If a
    secret already exists, this call will delete the old secret and create a new one.

    Args:
        authorization (str):
        json_body (CreateSecret):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SecretDetail
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
