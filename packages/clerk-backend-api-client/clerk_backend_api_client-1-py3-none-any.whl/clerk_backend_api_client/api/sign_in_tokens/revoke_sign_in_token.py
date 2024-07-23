from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.revoke_sign_in_token_response_200 import RevokeSignInTokenResponse200
from ...models.revoke_sign_in_token_response_400 import RevokeSignInTokenResponse400
from ...models.revoke_sign_in_token_response_404 import RevokeSignInTokenResponse404
from ...types import Response


def _get_kwargs(
    sign_in_token_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/sign_in_tokens/{sign_in_token_id}/revoke",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RevokeSignInTokenResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RevokeSignInTokenResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RevokeSignInTokenResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sign_in_token_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]:
    """Revoke the given sign-in token

     Revokes a pending sign-in token

    Args:
        sign_in_token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]
    """

    kwargs = _get_kwargs(
        sign_in_token_id=sign_in_token_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sign_in_token_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]:
    """Revoke the given sign-in token

     Revokes a pending sign-in token

    Args:
        sign_in_token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]
    """

    return sync_detailed(
        sign_in_token_id=sign_in_token_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sign_in_token_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]:
    """Revoke the given sign-in token

     Revokes a pending sign-in token

    Args:
        sign_in_token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]
    """

    kwargs = _get_kwargs(
        sign_in_token_id=sign_in_token_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sign_in_token_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]]:
    """Revoke the given sign-in token

     Revokes a pending sign-in token

    Args:
        sign_in_token_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeSignInTokenResponse200, RevokeSignInTokenResponse400, RevokeSignInTokenResponse404]
    """

    return (
        await asyncio_detailed(
            sign_in_token_id=sign_in_token_id,
            client=client,
        )
    ).parsed
