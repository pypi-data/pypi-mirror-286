from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from typing import Union
from ...models.get_filter_set_response_200 import GetFilterSetResponse200
from typing import Optional
from typing import Dict


def _get_kwargs(
    id: str,
    *,
    version_number: Union[Unset, None, int] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}
    params["version_number"] = version_number

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/api/v1/filter-sets/{id}/".format(
            id=id,
        ),
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetFilterSetResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetFilterSetResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetFilterSetResponse200]:
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
    version_number: Union[Unset, None, int] = UNSET,
    authorization: str,
) -> Response[GetFilterSetResponse200]:
    """Get filter set

     Get details of a filter set.

    Args:
        id (str):
        version_number (Union[Unset, None, int]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFilterSetResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        version_number=version_number,
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
    version_number: Union[Unset, None, int] = UNSET,
    authorization: str,
) -> Optional[GetFilterSetResponse200]:
    """Get filter set

     Get details of a filter set.

    Args:
        id (str):
        version_number (Union[Unset, None, int]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFilterSetResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
        version_number=version_number,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    version_number: Union[Unset, None, int] = UNSET,
    authorization: str,
) -> Response[GetFilterSetResponse200]:
    """Get filter set

     Get details of a filter set.

    Args:
        id (str):
        version_number (Union[Unset, None, int]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFilterSetResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        version_number=version_number,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    version_number: Union[Unset, None, int] = UNSET,
    authorization: str,
) -> Optional[GetFilterSetResponse200]:
    """Get filter set

     Get details of a filter set.

    Args:
        id (str):
        version_number (Union[Unset, None, int]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFilterSetResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            version_number=version_number,
            authorization=authorization,
        )
    ).parsed
