from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.mutually_exclusive_study_collection_update import MutuallyExclusiveStudyCollectionUpdate
from ...types import Response


def _get_kwargs(
    *,
    body: MutuallyExclusiveStudyCollectionUpdate,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/study-collections/mutually-exclusive/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[MutuallyExclusiveStudyCollectionUpdate]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = MutuallyExclusiveStudyCollectionUpdate.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MutuallyExclusiveStudyCollectionUpdate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MutuallyExclusiveStudyCollectionUpdate,
    authorization: str,
) -> Response[MutuallyExclusiveStudyCollectionUpdate]:
    """Create a mutually exclusive study collection.

     Create a mutually exclusive study collection.
    - Studies and study collections must be created separately and then added to the mutually exclusive
    study collection.
    - Both the studies and the study collection must be in the same project.
    - You can only add draft studies to a mutually exclusive study collection.
    - Adding studies which are already in one study collection to another study
    collection will remove the study from the original study collection.

    Args:
        authorization (str):
        body (MutuallyExclusiveStudyCollectionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MutuallyExclusiveStudyCollectionUpdate]
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
    body: MutuallyExclusiveStudyCollectionUpdate,
    authorization: str,
) -> Optional[MutuallyExclusiveStudyCollectionUpdate]:
    """Create a mutually exclusive study collection.

     Create a mutually exclusive study collection.
    - Studies and study collections must be created separately and then added to the mutually exclusive
    study collection.
    - Both the studies and the study collection must be in the same project.
    - You can only add draft studies to a mutually exclusive study collection.
    - Adding studies which are already in one study collection to another study
    collection will remove the study from the original study collection.

    Args:
        authorization (str):
        body (MutuallyExclusiveStudyCollectionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MutuallyExclusiveStudyCollectionUpdate
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MutuallyExclusiveStudyCollectionUpdate,
    authorization: str,
) -> Response[MutuallyExclusiveStudyCollectionUpdate]:
    """Create a mutually exclusive study collection.

     Create a mutually exclusive study collection.
    - Studies and study collections must be created separately and then added to the mutually exclusive
    study collection.
    - Both the studies and the study collection must be in the same project.
    - You can only add draft studies to a mutually exclusive study collection.
    - Adding studies which are already in one study collection to another study
    collection will remove the study from the original study collection.

    Args:
        authorization (str):
        body (MutuallyExclusiveStudyCollectionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MutuallyExclusiveStudyCollectionUpdate]
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
    body: MutuallyExclusiveStudyCollectionUpdate,
    authorization: str,
) -> Optional[MutuallyExclusiveStudyCollectionUpdate]:
    """Create a mutually exclusive study collection.

     Create a mutually exclusive study collection.
    - Studies and study collections must be created separately and then added to the mutually exclusive
    study collection.
    - Both the studies and the study collection must be in the same project.
    - You can only add draft studies to a mutually exclusive study collection.
    - Adding studies which are already in one study collection to another study
    collection will remove the study from the original study collection.

    Args:
        authorization (str):
        body (MutuallyExclusiveStudyCollectionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MutuallyExclusiveStudyCollectionUpdate
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
