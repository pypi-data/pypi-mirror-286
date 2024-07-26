from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.clone_filter_set_response_201 import CloneFilterSetResponse201
from ...models.clone_filter_set_json_body import CloneFilterSetJsonBody
from typing import Dict


def _get_kwargs(
    id: str,
    *,
    json_body: CloneFilterSetJsonBody,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/filter-sets/{id}/clone/".format(
            id=id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


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
    json_body: CloneFilterSetJsonBody,
    authorization: str,
) -> Response[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        json_body (CloneFilterSetJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloneFilterSetResponse201]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
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
    json_body: CloneFilterSetJsonBody,
    authorization: str,
) -> Optional[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        json_body (CloneFilterSetJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloneFilterSetResponse201
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: CloneFilterSetJsonBody,
    authorization: str,
) -> Response[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        json_body (CloneFilterSetJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloneFilterSetResponse201]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: CloneFilterSetJsonBody,
    authorization: str,
) -> Optional[CloneFilterSetResponse201]:
    """Clone filter set

     Create a copy of a filter set.

    Args:
        id (str):
        authorization (str):
        json_body (CloneFilterSetJsonBody):

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
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
