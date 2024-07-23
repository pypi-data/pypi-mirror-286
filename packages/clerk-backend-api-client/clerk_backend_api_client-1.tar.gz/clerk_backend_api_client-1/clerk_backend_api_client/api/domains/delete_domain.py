from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_domain_response_200 import DeleteDomainResponse200
from ...models.delete_domain_response_403 import DeleteDomainResponse403
from ...models.delete_domain_response_404 import DeleteDomainResponse404
from ...types import Response


def _get_kwargs(
    domain_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/domains/{domain_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteDomainResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = DeleteDomainResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteDomainResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]:
    """Delete a satellite domain

     Deletes a satellite domain for the instance.
    It is currently not possible to delete the instance's primary domain.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]:
    """Delete a satellite domain

     Deletes a satellite domain for the instance.
    It is currently not possible to delete the instance's primary domain.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]
    """

    return sync_detailed(
        domain_id=domain_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]:
    """Delete a satellite domain

     Deletes a satellite domain for the instance.
    It is currently not possible to delete the instance's primary domain.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]
    """

    kwargs = _get_kwargs(
        domain_id=domain_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]]:
    """Delete a satellite domain

     Deletes a satellite domain for the instance.
    It is currently not possible to delete the instance's primary domain.

    Args:
        domain_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteDomainResponse200, DeleteDomainResponse403, DeleteDomainResponse404]
    """

    return (
        await asyncio_detailed(
            domain_id=domain_id,
            client=client,
        )
    ).parsed
