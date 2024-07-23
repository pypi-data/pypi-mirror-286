from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_organization_response_200 import GetOrganizationResponse200
from ...models.get_organization_response_403 import GetOrganizationResponse403
from ...models.get_organization_response_404 import GetOrganizationResponse404
from ...types import Response


def _get_kwargs(
    organization_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/organizations/{organization_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetOrganizationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = GetOrganizationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetOrganizationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]:
    """Retrieve an organization by ID or slug

     Fetches the organization whose ID or slug matches the provided `id_or_slug` URL query parameter.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]:
    """Retrieve an organization by ID or slug

     Fetches the organization whose ID or slug matches the provided `id_or_slug` URL query parameter.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]:
    """Retrieve an organization by ID or slug

     Fetches the organization whose ID or slug matches the provided `id_or_slug` URL query parameter.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]]:
    """Retrieve an organization by ID or slug

     Fetches the organization whose ID or slug matches the provided `id_or_slug` URL query parameter.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetOrganizationResponse200, GetOrganizationResponse403, GetOrganizationResponse404]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
        )
    ).parsed
