from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_study import CreateStudy
from ...models.study import Study
from ...types import Response


def _get_kwargs(
    *,
    body: CreateStudy,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/studies/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Study]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Study.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Study]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateStudy,
    authorization: str,
) -> Response[Study]:
    """Create a draft study

     Create a draft study. Publishing a study is a two step process, first create a draft study then
    publish it.

    ## Taskflow Studies:
    Taskflow studies are created in the same manner as regular studies, however instead of providing an
    **external_study_url**, you should
    provide an access_details array with **access_detail** objects instead, containing an external_url
    field and a total_allocation field.

    Args:
        authorization (str):
        body (CreateStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
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
    body: CreateStudy,
    authorization: str,
) -> Optional[Study]:
    """Create a draft study

     Create a draft study. Publishing a study is a two step process, first create a draft study then
    publish it.

    ## Taskflow Studies:
    Taskflow studies are created in the same manner as regular studies, however instead of providing an
    **external_study_url**, you should
    provide an access_details array with **access_detail** objects instead, containing an external_url
    field and a total_allocation field.

    Args:
        authorization (str):
        body (CreateStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateStudy,
    authorization: str,
) -> Response[Study]:
    """Create a draft study

     Create a draft study. Publishing a study is a two step process, first create a draft study then
    publish it.

    ## Taskflow Studies:
    Taskflow studies are created in the same manner as regular studies, however instead of providing an
    **external_study_url**, you should
    provide an access_details array with **access_detail** objects instead, containing an external_url
    field and a total_allocation field.

    Args:
        authorization (str):
        body (CreateStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
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
    body: CreateStudy,
    authorization: str,
) -> Optional[Study]:
    """Create a draft study

     Create a draft study. Publishing a study is a two step process, first create a draft study then
    publish it.

    ## Taskflow Studies:
    Taskflow studies are created in the same manner as regular studies, however instead of providing an
    **external_study_url**, you should
    provide an access_details array with **access_detail** objects instead, containing an external_url
    field and a total_allocation field.

    Args:
        authorization (str):
        body (CreateStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
