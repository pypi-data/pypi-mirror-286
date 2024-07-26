from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_study import BaseStudy
from ...models.study import Study
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: BaseStudy,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v1/studies/{id}/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Study]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Study.from_dict(response.json())

        return response_200
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
    id: str,
    *,
    client: AuthenticatedClient,
    body: BaseStudy,
    authorization: str,
) -> Response[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.com/hc/en-gb/articles/360009222553)
    - access_details: Sending an access_detail will add a new task and increase overall study places by
    the number in the total_allocation field. Sending both access_details and total_available_places
    will increase places on existing URLs by the number specified on the access_detail.

    Args:
        id (str):
        authorization (str):
        body (BaseStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
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
    body: BaseStudy,
    authorization: str,
) -> Optional[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.com/hc/en-gb/articles/360009222553)
    - access_details: Sending an access_detail will add a new task and increase overall study places by
    the number in the total_allocation field. Sending both access_details and total_available_places
    will increase places on existing URLs by the number specified on the access_detail.

    Args:
        id (str):
        authorization (str):
        body (BaseStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
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
    body: BaseStudy,
    authorization: str,
) -> Response[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.com/hc/en-gb/articles/360009222553)
    - access_details: Sending an access_detail will add a new task and increase overall study places by
    the number in the total_allocation field. Sending both access_details and total_available_places
    will increase places on existing URLs by the number specified on the access_detail.

    Args:
        id (str):
        authorization (str):
        body (BaseStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
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
    body: BaseStudy,
    authorization: str,
) -> Optional[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.com/hc/en-gb/articles/360009222553)
    - access_details: Sending an access_detail will add a new task and increase overall study places by
    the number in the total_allocation field. Sending both access_details and total_available_places
    will increase places on existing URLs by the number specified on the access_detail.

    Args:
        id (str):
        authorization (str):
        body (BaseStudy):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
