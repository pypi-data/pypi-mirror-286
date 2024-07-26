from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subscription_detail import SubscriptionDetail
from ...models.subscription_list import SubscriptionList
from ...types import Response


def _get_kwargs(
    *,
    body: SubscriptionDetail,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/hooks/subscriptions/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SubscriptionList]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = SubscriptionList.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SubscriptionList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SubscriptionDetail,
    authorization: str,
) -> Response[SubscriptionList]:
    """Create a subscription

     Create a subscription for an event type. When an event is triggered in the Prolific system, the hook
    will automatically notify the specified target URL.

    Before creating a subscription, you must ensure that you have created a secret for your workspace.

    Args:
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionList]
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
    body: SubscriptionDetail,
    authorization: str,
) -> Optional[SubscriptionList]:
    """Create a subscription

     Create a subscription for an event type. When an event is triggered in the Prolific system, the hook
    will automatically notify the specified target URL.

    Before creating a subscription, you must ensure that you have created a secret for your workspace.

    Args:
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionList
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SubscriptionDetail,
    authorization: str,
) -> Response[SubscriptionList]:
    """Create a subscription

     Create a subscription for an event type. When an event is triggered in the Prolific system, the hook
    will automatically notify the specified target URL.

    Before creating a subscription, you must ensure that you have created a secret for your workspace.

    Args:
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubscriptionList]
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
    body: SubscriptionDetail,
    authorization: str,
) -> Optional[SubscriptionList]:
    """Create a subscription

     Create a subscription for an event type. When an event is triggered in the Prolific system, the hook
    will automatically notify the specified target URL.

    Before creating a subscription, you must ensure that you have created a secret for your workspace.

    Args:
        authorization (str):
        body (SubscriptionDetail):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubscriptionList
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
