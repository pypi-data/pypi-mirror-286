from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.create_filter_set_response_201 import CreateFilterSetResponse201
from typing import Dict
from ...models.create_filter_set import CreateFilterSet


def _get_kwargs(
    *,
    json_body: CreateFilterSet,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/filter-sets/",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CreateFilterSetResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateFilterSetResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateFilterSetResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Response[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFilterSetResponse201]
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
    json_body: CreateFilterSet,
    authorization: str,
) -> Optional[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFilterSetResponse201
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: CreateFilterSet,
    authorization: str,
) -> Response[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateFilterSetResponse201]
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
    json_body: CreateFilterSet,
    authorization: str,
) -> Optional[CreateFilterSetResponse201]:
    """Create filter set

     Create a filter set from a list of filters

    Args:
        authorization (str):
        json_body (CreateFilterSet):  Example: [{'workspace_id': '644aaabfaf6bbc363b9d47c6',
            'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness', 'selected_values':
            ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateFilterSetResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
