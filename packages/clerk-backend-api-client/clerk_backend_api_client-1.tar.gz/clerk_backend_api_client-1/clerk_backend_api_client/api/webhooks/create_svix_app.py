from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_svix_app_response_200 import CreateSvixAppResponse200
from ...models.create_svix_app_response_400 import CreateSvixAppResponse400
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/webhooks/svix",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateSvixAppResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateSvixAppResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]:
    """Create a Svix app

     Create a Svix app and associate it with the current instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]:
    """Create a Svix app

     Create a Svix app and associate it with the current instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSvixAppResponse200, CreateSvixAppResponse400]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]:
    """Create a Svix app

     Create a Svix app and associate it with the current instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[CreateSvixAppResponse200, CreateSvixAppResponse400]]:
    """Create a Svix app

     Create a Svix app and associate it with the current instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSvixAppResponse200, CreateSvixAppResponse400]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
