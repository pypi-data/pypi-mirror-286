from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.study_transition import StudyTransition
from typing import Dict
from ...models.study import Study


def _get_kwargs(
    id: str,
    *,
    json_body: StudyTransition,
    authorization: str,
) -> Dict[str, Any]:
    headers = {}
    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/api/v1/studies/{id}/transition/".format(
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
    json_body: StudyTransition,
    authorization: str,
) -> Response[Study]:
    """Publish a draft study

     Once the study is published, participants can partake in your experiment or survey.

    There are other status transitions available once the study is published:
    - PAUSE: Pause the study
    - START: Start a paused study
    - STOP: Stop a study completely, to make it active again you will need to increase the number of
    places

    To learn more about it check out [help center](https://researcher-help.prolific.com/hc/en-
    gb/articles/360010963354)

    Args:
        id (str):
        authorization (str):
        json_body (StudyTransition):

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
    json_body: StudyTransition,
    authorization: str,
) -> Optional[Study]:
    """Publish a draft study

     Once the study is published, participants can partake in your experiment or survey.

    There are other status transitions available once the study is published:
    - PAUSE: Pause the study
    - START: Start a paused study
    - STOP: Stop a study completely, to make it active again you will need to increase the number of
    places

    To learn more about it check out [help center](https://researcher-help.prolific.com/hc/en-
    gb/articles/360010963354)

    Args:
        id (str):
        authorization (str):
        json_body (StudyTransition):

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
    json_body: StudyTransition,
    authorization: str,
) -> Response[Study]:
    """Publish a draft study

     Once the study is published, participants can partake in your experiment or survey.

    There are other status transitions available once the study is published:
    - PAUSE: Pause the study
    - START: Start a paused study
    - STOP: Stop a study completely, to make it active again you will need to increase the number of
    places

    To learn more about it check out [help center](https://researcher-help.prolific.com/hc/en-
    gb/articles/360010963354)

    Args:
        id (str):
        authorization (str):
        json_body (StudyTransition):

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
    json_body: StudyTransition,
    authorization: str,
) -> Optional[Study]:
    """Publish a draft study

     Once the study is published, participants can partake in your experiment or survey.

    There are other status transitions available once the study is published:
    - PAUSE: Pause the study
    - START: Start a paused study
    - STOP: Stop a study completely, to make it active again you will need to increase the number of
    places

    To learn more about it check out [help center](https://researcher-help.prolific.com/hc/en-
    gb/articles/360010963354)

    Args:
        id (str):
        authorization (str):
        json_body (StudyTransition):

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
