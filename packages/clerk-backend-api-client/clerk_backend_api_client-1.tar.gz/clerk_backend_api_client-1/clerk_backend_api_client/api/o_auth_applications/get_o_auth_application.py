from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_o_auth_application_response_200 import GetOAuthApplicationResponse200
from ...models.get_o_auth_application_response_403 import GetOAuthApplicationResponse403
from ...models.get_o_auth_application_response_404 import GetOAuthApplicationResponse404
from ...types import Response


def _get_kwargs(
    oauth_application_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/oauth_applications/{oauth_application_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetOAuthApplicationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = GetOAuthApplicationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetOAuthApplicationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]:
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
) -> Response[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]:
    """Retrieve an OAuth application by ID

     Fetches the OAuth application whose ID matches the provided `id` in the path.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]
    """

    kwargs = _get_kwargs(
        oauth_application_id=oauth_application_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]:
    """Retrieve an OAuth application by ID

     Fetches the OAuth application whose ID matches the provided `id` in the path.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]
    """

    return sync_detailed(
        oauth_application_id=oauth_application_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]:
    """Retrieve an OAuth application by ID

     Fetches the OAuth application whose ID matches the provided `id` in the path.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]
    """

    kwargs = _get_kwargs(
        oauth_application_id=oauth_application_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]]:
    """Retrieve an OAuth application by ID

     Fetches the OAuth application whose ID matches the provided `id` in the path.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetOAuthApplicationResponse200, GetOAuthApplicationResponse403, GetOAuthApplicationResponse404]
    """

    return (
        await asyncio_detailed(
            oauth_application_id=oauth_application_id,
            client=client,
        )
    ).parsed
