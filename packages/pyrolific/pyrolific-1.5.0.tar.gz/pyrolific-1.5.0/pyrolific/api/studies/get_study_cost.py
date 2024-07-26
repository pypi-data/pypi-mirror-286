from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.study_total_cost import StudyTotalCost
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    is_projected: Union[Unset, bool] = False,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}

    params["is_projected"] = is_projected

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/studies/{id}/cost/",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[StudyTotalCost]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StudyTotalCost.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[StudyTotalCost]:
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
    is_projected: Union[Unset, bool] = False,
    authorization: str,
) -> Response[StudyTotalCost]:
    """Show Study cost

     Returns cost information about the study. Default behaviour is to return cost at the time of the
    request, but projected cost can be requested via a query parameter.

    Args:
        id (str):
        is_projected (Union[Unset, bool]):  Default: False.
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudyTotalCost]
    """

    kwargs = _get_kwargs(
        id=id,
        is_projected=is_projected,
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
    is_projected: Union[Unset, bool] = False,
    authorization: str,
) -> Optional[StudyTotalCost]:
    """Show Study cost

     Returns cost information about the study. Default behaviour is to return cost at the time of the
    request, but projected cost can be requested via a query parameter.

    Args:
        id (str):
        is_projected (Union[Unset, bool]):  Default: False.
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudyTotalCost
    """

    return sync_detailed(
        id=id,
        client=client,
        is_projected=is_projected,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    is_projected: Union[Unset, bool] = False,
    authorization: str,
) -> Response[StudyTotalCost]:
    """Show Study cost

     Returns cost information about the study. Default behaviour is to return cost at the time of the
    request, but projected cost can be requested via a query parameter.

    Args:
        id (str):
        is_projected (Union[Unset, bool]):  Default: False.
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudyTotalCost]
    """

    kwargs = _get_kwargs(
        id=id,
        is_projected=is_projected,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    is_projected: Union[Unset, bool] = False,
    authorization: str,
) -> Optional[StudyTotalCost]:
    """Show Study cost

     Returns cost information about the study. Default behaviour is to return cost at the time of the
    request, but projected cost can be requested via a query parameter.

    Args:
        id (str):
        is_projected (Union[Unset, bool]):  Default: False.
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudyTotalCost
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            is_projected=is_projected,
            authorization=authorization,
        )
    ).parsed
