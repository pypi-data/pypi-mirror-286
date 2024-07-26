from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.subscription_update_detail import SubscriptionUpdateDetail
from ...models.subscription_detail import SubscriptionDetail
from typing import Dict


def _get_kwargs(
    subscription_id: str,
    *,
    json_body: SubscriptionUpdateDetail,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": "/api/v1/hooks/subscriptions/{subscription_id}/".format(
            subscription_id=subscription_id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SubscriptionDetail]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SubscriptionDetail.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SubscriptionDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubscriptionUpdateDetail,
    authorization: str,
) -> Response[SubscriptionDetail]:
    """Update a subscription

     This allows you to update a subscription. For example you can temporarily disable a subscription if
    you wish.

    Args:
        subscription_id (str):
        authorization (str):
        json_body (SubscriptionUpdateDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDetail]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        json_body=json_body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubscriptionUpdateDetail,
    authorization: str,
) -> Optional[SubscriptionDetail]:
    """Update a subscription

     This allows you to update a subscription. For example you can temporarily disable a subscription if
    you wish.

    Args:
        subscription_id (str):
        authorization (str):
        json_body (SubscriptionUpdateDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDetail
    """

    return sync_detailed(
        subscription_id=subscription_id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubscriptionUpdateDetail,
    authorization: str,
) -> Response[SubscriptionDetail]:
    """Update a subscription

     This allows you to update a subscription. For example you can temporarily disable a subscription if
    you wish.

    Args:
        subscription_id (str):
        authorization (str):
        json_body (SubscriptionUpdateDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDetail]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        json_body=json_body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SubscriptionUpdateDetail,
    authorization: str,
) -> Optional[SubscriptionDetail]:
    """Update a subscription

     This allows you to update a subscription. For example you can temporarily disable a subscription if
    you wish.

    Args:
        subscription_id (str):
        authorization (str):
        json_body (SubscriptionUpdateDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDetail
    """

    return (
        await asyncio_detailed(
            subscription_id=subscription_id,
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
