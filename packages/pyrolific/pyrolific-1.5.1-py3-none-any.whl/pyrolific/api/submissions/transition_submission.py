from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.submission import Submission
from ...models.submission_transition import SubmissionTransition
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: SubmissionTransition,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/v1/submissions/{id}/transition/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Submission]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Submission.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Submission]:
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
    body: SubmissionTransition,
    authorization: str,
) -> Response[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED`, `REJECTED` or `AWAITING_REVIEW`. Once the status is changed,
    it can not be restored to its previous value.

    Note this endpoint is idempotent, so if you make the same request twice, the second request will be
    ignored.

    Args:
        id (str):
        authorization (str):
        body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Submission]
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
    body: SubmissionTransition,
    authorization: str,
) -> Optional[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED`, `REJECTED` or `AWAITING_REVIEW`. Once the status is changed,
    it can not be restored to its previous value.

    Note this endpoint is idempotent, so if you make the same request twice, the second request will be
    ignored.

    Args:
        id (str):
        authorization (str):
        body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Submission
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
    body: SubmissionTransition,
    authorization: str,
) -> Response[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED`, `REJECTED` or `AWAITING_REVIEW`. Once the status is changed,
    it can not be restored to its previous value.

    Note this endpoint is idempotent, so if you make the same request twice, the second request will be
    ignored.

    Args:
        id (str):
        authorization (str):
        body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Submission]
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
    body: SubmissionTransition,
    authorization: str,
) -> Optional[Submission]:
    """Approve or reject a submission

     Transition a submission to `APPROVED`, `REJECTED` or `AWAITING_REVIEW`. Once the status is changed,
    it can not be restored to its previous value.

    Note this endpoint is idempotent, so if you make the same request twice, the second request will be
    ignored.

    Args:
        id (str):
        authorization (str):
        body (SubmissionTransition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Submission
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
