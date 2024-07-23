from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_o_auth_application_body import UpdateOAuthApplicationBody
from ...models.update_o_auth_application_response_200 import UpdateOAuthApplicationResponse200
from ...models.update_o_auth_application_response_403 import UpdateOAuthApplicationResponse403
from ...models.update_o_auth_application_response_404 import UpdateOAuthApplicationResponse404
from ...models.update_o_auth_application_response_422 import UpdateOAuthApplicationResponse422
from ...types import Response


def _get_kwargs(
    oauth_application_id: str,
    *,
    body: UpdateOAuthApplicationBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/oauth_applications/{oauth_application_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        UpdateOAuthApplicationResponse200,
        UpdateOAuthApplicationResponse403,
        UpdateOAuthApplicationResponse404,
        UpdateOAuthApplicationResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateOAuthApplicationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UpdateOAuthApplicationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateOAuthApplicationResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateOAuthApplicationResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateOAuthApplicationResponse200,
        UpdateOAuthApplicationResponse403,
        UpdateOAuthApplicationResponse404,
        UpdateOAuthApplicationResponse422,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOAuthApplicationBody,
) -> Response[
    Union[
        UpdateOAuthApplicationResponse200,
        UpdateOAuthApplicationResponse403,
        UpdateOAuthApplicationResponse404,
        UpdateOAuthApplicationResponse422,
    ]
]:
    """Update an OAuth application

     Updates an existing OAuth application

    Args:
        oauth_application_id (str):
        body (UpdateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOAuthApplicationResponse200, UpdateOAuthApplicationResponse403, UpdateOAuthApplicationResponse404, UpdateOAuthApplicationResponse422]]
    """

    kwargs = _get_kwargs(
        oauth_application_id=oauth_application_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOAuthApplicationBody,
) -> Optional[
    Union[
        UpdateOAuthApplicationResponse200,
        UpdateOAuthApplicationResponse403,
        UpdateOAuthApplicationResponse404,
        UpdateOAuthApplicationResponse422,
    ]
]:
    """Update an OAuth application

     Updates an existing OAuth application

    Args:
        oauth_application_id (str):
        body (UpdateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOAuthApplicationResponse200, UpdateOAuthApplicationResponse403, UpdateOAuthApplicationResponse404, UpdateOAuthApplicationResponse422]
    """

    return sync_detailed(
        oauth_application_id=oauth_application_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOAuthApplicationBody,
) -> Response[
    Union[
        UpdateOAuthApplicationResponse200,
        UpdateOAuthApplicationResponse403,
        UpdateOAuthApplicationResponse404,
        UpdateOAuthApplicationResponse422,
    ]
]:
    """Update an OAuth application

     Updates an existing OAuth application

    Args:
        oauth_application_id (str):
        body (UpdateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOAuthApplicationResponse200, UpdateOAuthApplicationResponse403, UpdateOAuthApplicationResponse404, UpdateOAuthApplicationResponse422]]
    """

    kwargs = _get_kwargs(
        oauth_application_id=oauth_application_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOAuthApplicationBody,
) -> Optional[
    Union[
        UpdateOAuthApplicationResponse200,
        UpdateOAuthApplicationResponse403,
        UpdateOAuthApplicationResponse404,
        UpdateOAuthApplicationResponse422,
    ]
]:
    """Update an OAuth application

     Updates an existing OAuth application

    Args:
        oauth_application_id (str):
        body (UpdateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOAuthApplicationResponse200, UpdateOAuthApplicationResponse403, UpdateOAuthApplicationResponse404, UpdateOAuthApplicationResponse422]
    """

    return (
        await asyncio_detailed(
            oauth_application_id=oauth_application_id,
            client=client,
            body=body,
        )
    ).parsed
