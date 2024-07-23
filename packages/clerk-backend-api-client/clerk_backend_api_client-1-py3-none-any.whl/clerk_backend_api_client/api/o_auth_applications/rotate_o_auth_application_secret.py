from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rotate_o_auth_application_secret_response_200 import RotateOAuthApplicationSecretResponse200
from ...models.rotate_o_auth_application_secret_response_403 import RotateOAuthApplicationSecretResponse403
from ...models.rotate_o_auth_application_secret_response_404 import RotateOAuthApplicationSecretResponse404
from ...types import Response


def _get_kwargs(
    oauth_application_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/oauth_applications/{oauth_application_id}/rotate_secret",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        RotateOAuthApplicationSecretResponse200,
        RotateOAuthApplicationSecretResponse403,
        RotateOAuthApplicationSecretResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RotateOAuthApplicationSecretResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = RotateOAuthApplicationSecretResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RotateOAuthApplicationSecretResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        RotateOAuthApplicationSecretResponse200,
        RotateOAuthApplicationSecretResponse403,
        RotateOAuthApplicationSecretResponse404,
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
) -> Response[
    Union[
        RotateOAuthApplicationSecretResponse200,
        RotateOAuthApplicationSecretResponse403,
        RotateOAuthApplicationSecretResponse404,
    ]
]:
    """Rotate the client secret of the given OAuth application

     Rotates the OAuth application's client secret.
    When the client secret is rotated, make sure to update it in authorized OAuth clients.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RotateOAuthApplicationSecretResponse200, RotateOAuthApplicationSecretResponse403, RotateOAuthApplicationSecretResponse404]]
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
) -> Optional[
    Union[
        RotateOAuthApplicationSecretResponse200,
        RotateOAuthApplicationSecretResponse403,
        RotateOAuthApplicationSecretResponse404,
    ]
]:
    """Rotate the client secret of the given OAuth application

     Rotates the OAuth application's client secret.
    When the client secret is rotated, make sure to update it in authorized OAuth clients.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RotateOAuthApplicationSecretResponse200, RotateOAuthApplicationSecretResponse403, RotateOAuthApplicationSecretResponse404]
    """

    return sync_detailed(
        oauth_application_id=oauth_application_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    oauth_application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        RotateOAuthApplicationSecretResponse200,
        RotateOAuthApplicationSecretResponse403,
        RotateOAuthApplicationSecretResponse404,
    ]
]:
    """Rotate the client secret of the given OAuth application

     Rotates the OAuth application's client secret.
    When the client secret is rotated, make sure to update it in authorized OAuth clients.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RotateOAuthApplicationSecretResponse200, RotateOAuthApplicationSecretResponse403, RotateOAuthApplicationSecretResponse404]]
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
) -> Optional[
    Union[
        RotateOAuthApplicationSecretResponse200,
        RotateOAuthApplicationSecretResponse403,
        RotateOAuthApplicationSecretResponse404,
    ]
]:
    """Rotate the client secret of the given OAuth application

     Rotates the OAuth application's client secret.
    When the client secret is rotated, make sure to update it in authorized OAuth clients.

    Args:
        oauth_application_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RotateOAuthApplicationSecretResponse200, RotateOAuthApplicationSecretResponse403, RotateOAuthApplicationSecretResponse404]
    """

    return (
        await asyncio_detailed(
            oauth_application_id=oauth_application_id,
            client=client,
        )
    ).parsed
