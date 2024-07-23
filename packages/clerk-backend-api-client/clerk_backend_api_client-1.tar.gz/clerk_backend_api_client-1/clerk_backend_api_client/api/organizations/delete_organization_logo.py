from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_organization_logo_response_200 import DeleteOrganizationLogoResponse200
from ...models.delete_organization_logo_response_404 import DeleteOrganizationLogoResponse404
from ...types import Response


def _get_kwargs(
    organization_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/organizations/{organization_id}/logo",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteOrganizationLogoResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteOrganizationLogoResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]:
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
) -> Response[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]:
    """Delete the organization's logo.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]
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
) -> Optional[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]:
    """Delete the organization's logo.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]:
    """Delete the organization's logo.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]
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
) -> Optional[Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]]:
    """Delete the organization's logo.

    Args:
        organization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteOrganizationLogoResponse200, DeleteOrganizationLogoResponse404]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
        )
    ).parsed
