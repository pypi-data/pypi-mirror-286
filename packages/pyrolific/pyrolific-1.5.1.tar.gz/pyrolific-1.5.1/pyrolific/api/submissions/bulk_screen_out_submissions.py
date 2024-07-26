from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_screen_out_request import BulkScreenOutRequest
from ...models.bulk_screen_out_submissions_response_202 import BulkScreenOutSubmissionsResponse202
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: BulkScreenOutRequest,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/v1/submissions/bulk-screen-out/{id}/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[BulkScreenOutSubmissionsResponse202]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = BulkScreenOutSubmissionsResponse202.from_dict(response.json())

        return response_202
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[BulkScreenOutSubmissionsResponse202]:
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
    body: BulkScreenOutRequest,
    authorization: str,
) -> Response[BulkScreenOutSubmissionsResponse202]:
    """Bulk screen out submissions

     This endpoint is designed to be used as part of a custom screening study.
    If a participant has taken part in a study where you have asked screening questions
    and has not met your screening requirements, this endpoint allows you to screen out
    multiple participants at once.
    The endpoint accepts a list of submission ID's and a bonus amount and will perform the following
    actions:
    - Change the status of the submission to `SCREENED_OUT` which is equivalent to returning the
    submission.
    - Pay the participant a bonus, specified by you.
    - Send the participant a message explaining that they have been screened out and showing their bonus
    amount.
    All submission ID's must belong to the specified study. Bonus per submission is a decimal value in
    your study
    currency, e.g. 1.50 for £1.50.

    Args:
        id (str):
        authorization (str):
        body (BulkScreenOutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkScreenOutSubmissionsResponse202]
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
    body: BulkScreenOutRequest,
    authorization: str,
) -> Optional[BulkScreenOutSubmissionsResponse202]:
    """Bulk screen out submissions

     This endpoint is designed to be used as part of a custom screening study.
    If a participant has taken part in a study where you have asked screening questions
    and has not met your screening requirements, this endpoint allows you to screen out
    multiple participants at once.
    The endpoint accepts a list of submission ID's and a bonus amount and will perform the following
    actions:
    - Change the status of the submission to `SCREENED_OUT` which is equivalent to returning the
    submission.
    - Pay the participant a bonus, specified by you.
    - Send the participant a message explaining that they have been screened out and showing their bonus
    amount.
    All submission ID's must belong to the specified study. Bonus per submission is a decimal value in
    your study
    currency, e.g. 1.50 for £1.50.

    Args:
        id (str):
        authorization (str):
        body (BulkScreenOutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkScreenOutSubmissionsResponse202
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
    body: BulkScreenOutRequest,
    authorization: str,
) -> Response[BulkScreenOutSubmissionsResponse202]:
    """Bulk screen out submissions

     This endpoint is designed to be used as part of a custom screening study.
    If a participant has taken part in a study where you have asked screening questions
    and has not met your screening requirements, this endpoint allows you to screen out
    multiple participants at once.
    The endpoint accepts a list of submission ID's and a bonus amount and will perform the following
    actions:
    - Change the status of the submission to `SCREENED_OUT` which is equivalent to returning the
    submission.
    - Pay the participant a bonus, specified by you.
    - Send the participant a message explaining that they have been screened out and showing their bonus
    amount.
    All submission ID's must belong to the specified study. Bonus per submission is a decimal value in
    your study
    currency, e.g. 1.50 for £1.50.

    Args:
        id (str):
        authorization (str):
        body (BulkScreenOutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkScreenOutSubmissionsResponse202]
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
    body: BulkScreenOutRequest,
    authorization: str,
) -> Optional[BulkScreenOutSubmissionsResponse202]:
    """Bulk screen out submissions

     This endpoint is designed to be used as part of a custom screening study.
    If a participant has taken part in a study where you have asked screening questions
    and has not met your screening requirements, this endpoint allows you to screen out
    multiple participants at once.
    The endpoint accepts a list of submission ID's and a bonus amount and will perform the following
    actions:
    - Change the status of the submission to `SCREENED_OUT` which is equivalent to returning the
    submission.
    - Pay the participant a bonus, specified by you.
    - Send the participant a message explaining that they have been screened out and showing their bonus
    amount.
    All submission ID's must belong to the specified study. Bonus per submission is a decimal value in
    your study
    currency, e.g. 1.50 for £1.50.

    Args:
        id (str):
        authorization (str):
        body (BulkScreenOutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkScreenOutSubmissionsResponse202
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
