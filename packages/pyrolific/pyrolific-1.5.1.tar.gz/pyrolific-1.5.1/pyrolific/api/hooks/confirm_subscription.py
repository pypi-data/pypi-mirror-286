from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subscription_detail import SubscriptionDetail
from ...types import Response


def _get_kwargs(
    subscription_id: str,
    *,
    body: SubscriptionDetail,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/v1/hooks/subscriptions/{subscription_id}/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


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
    body: SubscriptionDetail,
    authorization: str,
) -> Response[SubscriptionDetail]:
    """Confirm a subscription

     Confirm a subscription to an event type

    Args:
        subscription_id (str):
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDetail]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        body=body,
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
    body: SubscriptionDetail,
    authorization: str,
) -> Optional[SubscriptionDetail]:
    """Confirm a subscription

     Confirm a subscription to an event type

    Args:
        subscription_id (str):
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionDetail
    """

    return sync_detailed(
        subscription_id=subscription_id,
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    body: SubscriptionDetail,
    authorization: str,
) -> Response[SubscriptionDetail]:
    """Confirm a subscription

     Confirm a subscription to an event type

    Args:
        subscription_id (str):
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionDetail]
    """

    kwargs = _get_kwargs(
        subscription_id=subscription_id,
        body=body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subscription_id: str,
    *,
    client: AuthenticatedClient,
    body: SubscriptionDetail,
    authorization: str,
) -> Optional[SubscriptionDetail]:
    """Confirm a subscription

     Confirm a subscription to an event type

    Args:
        subscription_id (str):
        authorization (str):
        body (SubscriptionDetail):

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
            body=body,
            authorization=authorization,
        )
    ).parsed
