from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_sign_in_token_body import CreateSignInTokenBody
from ...models.create_sign_in_token_response_200 import CreateSignInTokenResponse200
from ...models.create_sign_in_token_response_404 import CreateSignInTokenResponse404
from ...models.create_sign_in_token_response_422 import CreateSignInTokenResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateSignInTokenBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/sign_in_tokens",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateSignInTokenResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateSignInTokenResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateSignInTokenResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSignInTokenBody,
) -> Response[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]:
    """Create sign-in token

     Creates a new sign-in token and associates it with the given user.
    By default, sign-in tokens expire in 30 days.
    You can optionally supply a different duration in seconds using the `expires_in_seconds` property.

    Args:
        body (CreateSignInTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSignInTokenBody,
) -> Optional[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]:
    """Create sign-in token

     Creates a new sign-in token and associates it with the given user.
    By default, sign-in tokens expire in 30 days.
    You can optionally supply a different duration in seconds using the `expires_in_seconds` property.

    Args:
        body (CreateSignInTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSignInTokenBody,
) -> Response[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]:
    """Create sign-in token

     Creates a new sign-in token and associates it with the given user.
    By default, sign-in tokens expire in 30 days.
    You can optionally supply a different duration in seconds using the `expires_in_seconds` property.

    Args:
        body (CreateSignInTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateSignInTokenBody,
) -> Optional[Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]]:
    """Create sign-in token

     Creates a new sign-in token and associates it with the given user.
    By default, sign-in tokens expire in 30 days.
    You can optionally supply a different duration in seconds using the `expires_in_seconds` property.

    Args:
        body (CreateSignInTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSignInTokenResponse200, CreateSignInTokenResponse404, CreateSignInTokenResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
