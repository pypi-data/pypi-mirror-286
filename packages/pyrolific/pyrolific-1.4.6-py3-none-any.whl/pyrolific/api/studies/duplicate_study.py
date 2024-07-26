from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from typing import Dict
from ...models.duplicate_study_json_body import DuplicateStudyJsonBody
from ...models.study import Study


def _get_kwargs(
    id: str,
    *,
    json_body: DuplicateStudyJsonBody,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/studies/{id}/clone/".format(
            id=id,
        ),
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Study]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Study.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Study]:
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
    json_body: DuplicateStudyJsonBody,
    authorization: str,
) -> Response[Study]:
    """Duplicate a study

     Duplicating a study can save a lot of time and effort compared to creating a new study from scratch,
    since all of the information and data from the original study will be carried over to the new study.
    Additionally, duplicating a study can help ensure that the new study is set up consistently with the
    original, reducing the risk of errors or inconsistencies.

    To prevent repeat participation, a block list containing the original study will be added to the
    duplicated study's filters unless `block_previous_participants` is set to `false` in the request
    body.

    Args:
        id (str):
        authorization (str):
        json_body (DuplicateStudyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
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
    json_body: DuplicateStudyJsonBody,
    authorization: str,
) -> Optional[Study]:
    """Duplicate a study

     Duplicating a study can save a lot of time and effort compared to creating a new study from scratch,
    since all of the information and data from the original study will be carried over to the new study.
    Additionally, duplicating a study can help ensure that the new study is set up consistently with the
    original, reducing the risk of errors or inconsistencies.

    To prevent repeat participation, a block list containing the original study will be added to the
    duplicated study's filters unless `block_previous_participants` is set to `false` in the request
    body.

    Args:
        id (str):
        authorization (str):
        json_body (DuplicateStudyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
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
    json_body: DuplicateStudyJsonBody,
    authorization: str,
) -> Response[Study]:
    """Duplicate a study

     Duplicating a study can save a lot of time and effort compared to creating a new study from scratch,
    since all of the information and data from the original study will be carried over to the new study.
    Additionally, duplicating a study can help ensure that the new study is set up consistently with the
    original, reducing the risk of errors or inconsistencies.

    To prevent repeat participation, a block list containing the original study will be added to the
    duplicated study's filters unless `block_previous_participants` is set to `false` in the request
    body.

    Args:
        id (str):
        authorization (str):
        json_body (DuplicateStudyJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
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
    json_body: DuplicateStudyJsonBody,
    authorization: str,
) -> Optional[Study]:
    """Duplicate a study

     Duplicating a study can save a lot of time and effort compared to creating a new study from scratch,
    since all of the information and data from the original study will be carried over to the new study.
    Additionally, duplicating a study can help ensure that the new study is set up consistently with the
    original, reducing the risk of errors or inconsistencies.

    To prevent repeat participation, a block list containing the original study will be added to the
    duplicated study's filters unless `block_previous_participants` is set to `false` in the request
    body.

    Args:
        id (str):
        authorization (str):
        json_body (DuplicateStudyJsonBody):

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
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
