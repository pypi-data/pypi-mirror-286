from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_studies_state import GetStudiesState
from ...models.studies_list_response import StudiesListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    state: Union[Unset, GetStudiesState] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/studies/",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[StudiesListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StudiesListResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[StudiesListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, GetStudiesState] = UNSET,
    authorization: str,
) -> Response[StudiesListResponse]:
    """List all studies

     List all studies, with the option to filter by study status.

    Args:
        state (Union[Unset, GetStudiesState]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudiesListResponse]
    """

    kwargs = _get_kwargs(
        state=state,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, GetStudiesState] = UNSET,
    authorization: str,
) -> Optional[StudiesListResponse]:
    """List all studies

     List all studies, with the option to filter by study status.

    Args:
        state (Union[Unset, GetStudiesState]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudiesListResponse
    """

    return sync_detailed(
        client=client,
        state=state,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, GetStudiesState] = UNSET,
    authorization: str,
) -> Response[StudiesListResponse]:
    """List all studies

     List all studies, with the option to filter by study status.

    Args:
        state (Union[Unset, GetStudiesState]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudiesListResponse]
    """

    kwargs = _get_kwargs(
        state=state,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    state: Union[Unset, GetStudiesState] = UNSET,
    authorization: str,
) -> Optional[StudiesListResponse]:
    """List all studies

     List all studies, with the option to filter by study status.

    Args:
        state (Union[Unset, GetStudiesState]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudiesListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            state=state,
            authorization=authorization,
        )
    ).parsed
