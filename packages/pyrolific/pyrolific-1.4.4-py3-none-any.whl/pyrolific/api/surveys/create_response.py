from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.response_out import ResponseOut
from ...models.response_in import ResponseIn
from typing import Dict


def _get_kwargs(
    survey_id: str,
    *,
    json_body: ResponseIn,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/surveys/{survey_id}/responses/".format(
            survey_id=survey_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResponseOut]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ResponseOut.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResponseOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ResponseIn,
) -> Response[ResponseOut]:
    """Create response

     Create a Response for a survey.

    Args:
        survey_id (str):
        json_body (ResponseIn): The model used to create a `Response`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseOut]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ResponseIn,
) -> Optional[ResponseOut]:
    """Create response

     Create a Response for a survey.

    Args:
        survey_id (str):
        json_body (ResponseIn): The model used to create a `Response`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseOut
    """

    return sync_detailed(
        survey_id=survey_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ResponseIn,
) -> Response[ResponseOut]:
    """Create response

     Create a Response for a survey.

    Args:
        survey_id (str):
        json_body (ResponseIn): The model used to create a `Response`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseOut]
    """

    kwargs = _get_kwargs(
        survey_id=survey_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    survey_id: str,
    *,
    client: AuthenticatedClient,
    json_body: ResponseIn,
) -> Optional[ResponseOut]:
    """Create response

     Create a Response for a survey.

    Args:
        survey_id (str):
        json_body (ResponseIn): The model used to create a `Response`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseOut
    """

    return (
        await asyncio_detailed(
            survey_id=survey_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
