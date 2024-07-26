from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clone_filter_set_body import CloneFilterSetBody
from ...models.clone_filter_set_response_201 import CloneFilterSetResponse201
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: CloneFilterSetBody,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/v1/filter-sets/{id}/clone/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CloneFilterSetResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CloneFilterSetResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CloneFilterSetResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: CloneFilterSetBody,
    authorization: str,
) -> Response[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        body (CloneFilterSetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloneFilterSetResponse201]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: CloneFilterSetBody,
    authorization: str,
) -> Optional[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        body (CloneFilterSetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloneFilterSetResponse201
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: CloneFilterSetBody,
    authorization: str,
) -> Response[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        body (CloneFilterSetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloneFilterSetResponse201]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: CloneFilterSetBody,
    authorization: str,
) -> Optional[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        body (CloneFilterSetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloneFilterSetResponse201
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
