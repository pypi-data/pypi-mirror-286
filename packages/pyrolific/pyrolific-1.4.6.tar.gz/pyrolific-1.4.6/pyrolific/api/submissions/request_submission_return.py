from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.request_submission_return_json_body import (
    RequestSubmissionReturnJsonBody,
)
from typing import Dict
from ...models.return_requested_response import ReturnRequestedResponse


def _get_kwargs(
    id: str,
    *,
    json_body: RequestSubmissionReturnJsonBody,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/submissions/{id}/request-return/".format(
            id=id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ReturnRequestedResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ReturnRequestedResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReturnRequestedResponse]:
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
    json_body: RequestSubmissionReturnJsonBody,
) -> Response[ReturnRequestedResponse]:
    r"""Request the participant who submitted the response to return their response

     **This is an experimental feature that may be subject to change in the future.** <br/>
    It offers researchers the ability to ask a participant to return a submission. The return reason
    must be provided in the request and can be any free text string. <br/> The Prolific UI allows users
    to select any of the following options:
    * Didn't finish the study
    * Encountered technical problems
    * Withdrew consent
    * Other ( uses the free text input)

    This constructs a message around the reasons provided so there is no need to provide additional text
    beyond the reasons.
    <img alt=\"Example\" src=\"/assets/img/api/message.png\" />

    Args:
        id (str):
        json_body (RequestSubmissionReturnJsonBody):  Example: {'request_return_reasons':
            ['Withdrew consent.', 'Did not finish study.']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReturnRequestedResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: RequestSubmissionReturnJsonBody,
) -> Optional[ReturnRequestedResponse]:
    r"""Request the participant who submitted the response to return their response

     **This is an experimental feature that may be subject to change in the future.** <br/>
    It offers researchers the ability to ask a participant to return a submission. The return reason
    must be provided in the request and can be any free text string. <br/> The Prolific UI allows users
    to select any of the following options:
    * Didn't finish the study
    * Encountered technical problems
    * Withdrew consent
    * Other ( uses the free text input)

    This constructs a message around the reasons provided so there is no need to provide additional text
    beyond the reasons.
    <img alt=\"Example\" src=\"/assets/img/api/message.png\" />

    Args:
        id (str):
        json_body (RequestSubmissionReturnJsonBody):  Example: {'request_return_reasons':
            ['Withdrew consent.', 'Did not finish study.']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReturnRequestedResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: RequestSubmissionReturnJsonBody,
) -> Response[ReturnRequestedResponse]:
    r"""Request the participant who submitted the response to return their response

     **This is an experimental feature that may be subject to change in the future.** <br/>
    It offers researchers the ability to ask a participant to return a submission. The return reason
    must be provided in the request and can be any free text string. <br/> The Prolific UI allows users
    to select any of the following options:
    * Didn't finish the study
    * Encountered technical problems
    * Withdrew consent
    * Other ( uses the free text input)

    This constructs a message around the reasons provided so there is no need to provide additional text
    beyond the reasons.
    <img alt=\"Example\" src=\"/assets/img/api/message.png\" />

    Args:
        id (str):
        json_body (RequestSubmissionReturnJsonBody):  Example: {'request_return_reasons':
            ['Withdrew consent.', 'Did not finish study.']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReturnRequestedResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: RequestSubmissionReturnJsonBody,
) -> Optional[ReturnRequestedResponse]:
    r"""Request the participant who submitted the response to return their response

     **This is an experimental feature that may be subject to change in the future.** <br/>
    It offers researchers the ability to ask a participant to return a submission. The return reason
    must be provided in the request and can be any free text string. <br/> The Prolific UI allows users
    to select any of the following options:
    * Didn't finish the study
    * Encountered technical problems
    * Withdrew consent
    * Other ( uses the free text input)

    This constructs a message around the reasons provided so there is no need to provide additional text
    beyond the reasons.
    <img alt=\"Example\" src=\"/assets/img/api/message.png\" />

    Args:
        id (str):
        json_body (RequestSubmissionReturnJsonBody):  Example: {'request_return_reasons':
            ['Withdrew consent.', 'Did not finish study.']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReturnRequestedResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
