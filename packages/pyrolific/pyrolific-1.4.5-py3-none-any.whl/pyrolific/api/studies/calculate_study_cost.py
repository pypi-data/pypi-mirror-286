from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.study_cost_request import StudyCostRequest
from ...models.study_cost_response import StudyCostResponse
from typing import Dict


def _get_kwargs(
    *,
    json_body: StudyCostRequest,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/study-cost-calculator/",
        "json": json_json_body,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[StudyCostResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = StudyCostResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[StudyCostResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: StudyCostRequest,
    authorization: str,
) -> Response[StudyCostResponse]:
    """Calculate the study cost

     Calculate the study cost, including VAT and fees.

    Args:
        authorization (str):
        json_body (StudyCostRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudyCostResponse]
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
    json_body: StudyCostRequest,
    authorization: str,
) -> Optional[StudyCostResponse]:
    """Calculate the study cost

     Calculate the study cost, including VAT and fees.

    Args:
        authorization (str):
        json_body (StudyCostRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudyCostResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: StudyCostRequest,
    authorization: str,
) -> Response[StudyCostResponse]:
    """Calculate the study cost

     Calculate the study cost, including VAT and fees.

    Args:
        authorization (str):
        json_body (StudyCostRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StudyCostResponse]
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
    json_body: StudyCostRequest,
    authorization: str,
) -> Optional[StudyCostResponse]:
    """Calculate the study cost

     Calculate the study cost, including VAT and fees.

    Args:
        authorization (str):
        json_body (StudyCostRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StudyCostResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed
