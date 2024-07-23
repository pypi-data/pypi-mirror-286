from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_domains_response_200 import ListDomainsResponse200
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/domains",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListDomainsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListDomainsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListDomainsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListDomainsResponse200]:
    """List all instance domains

     Use this endpoint to get a list of all domains for an instance.
    The response will contain the primary domain for the instance and any satellite domains. Each domain
    in the response contains information about the URLs where Clerk operates and the required CNAME
    targets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDomainsResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListDomainsResponse200]:
    """List all instance domains

     Use this endpoint to get a list of all domains for an instance.
    The response will contain the primary domain for the instance and any satellite domains. Each domain
    in the response contains information about the URLs where Clerk operates and the required CNAME
    targets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDomainsResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListDomainsResponse200]:
    """List all instance domains

     Use this endpoint to get a list of all domains for an instance.
    The response will contain the primary domain for the instance and any satellite domains. Each domain
    in the response contains information about the URLs where Clerk operates and the required CNAME
    targets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDomainsResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListDomainsResponse200]:
    """List all instance domains

     Use this endpoint to get a list of all domains for an instance.
    The response will contain the primary domain for the instance and any satellite domains. Each domain
    in the response contains information about the URLs where Clerk operates and the required CNAME
    targets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDomainsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
