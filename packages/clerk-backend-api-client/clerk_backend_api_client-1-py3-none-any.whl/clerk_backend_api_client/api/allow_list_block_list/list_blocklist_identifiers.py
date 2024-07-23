from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_blocklist_identifiers_response_200 import ListBlocklistIdentifiersResponse200
from ...models.list_blocklist_identifiers_response_401 import ListBlocklistIdentifiersResponse401
from ...models.list_blocklist_identifiers_response_402 import ListBlocklistIdentifiersResponse402
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/blocklist_identifiers",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListBlocklistIdentifiersResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListBlocklistIdentifiersResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = ListBlocklistIdentifiersResponse402.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
]:
    """List all identifiers on the block-list

     Get a list of all identifiers which are not allowed to access an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
]:
    """List all identifiers on the block-list

     Get a list of all identifiers which are not allowed to access an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
]:
    """List all identifiers on the block-list

     Get a list of all identifiers which are not allowed to access an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
]:
    """List all identifiers on the block-list

     Get a list of all identifiers which are not allowed to access an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListBlocklistIdentifiersResponse200, ListBlocklistIdentifiersResponse401, ListBlocklistIdentifiersResponse402]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
