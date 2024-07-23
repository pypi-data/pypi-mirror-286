from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_allowlist_identifiers_response_200_item import ListAllowlistIdentifiersResponse200Item
from ...models.list_allowlist_identifiers_response_401 import ListAllowlistIdentifiersResponse401
from ...models.list_allowlist_identifiers_response_402 import ListAllowlistIdentifiersResponse402
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/allowlist_identifiers",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ListAllowlistIdentifiersResponse401,
        ListAllowlistIdentifiersResponse402,
        List["ListAllowlistIdentifiersResponse200Item"],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListAllowlistIdentifiersResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListAllowlistIdentifiersResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = ListAllowlistIdentifiersResponse402.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ListAllowlistIdentifiersResponse401,
        ListAllowlistIdentifiersResponse402,
        List["ListAllowlistIdentifiersResponse200Item"],
    ]
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
    Union[
        ListAllowlistIdentifiersResponse401,
        ListAllowlistIdentifiersResponse402,
        List["ListAllowlistIdentifiersResponse200Item"],
    ]
]:
    """List all identifiers on the allow-list

     Get a list of all identifiers allowed to sign up to an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListAllowlistIdentifiersResponse401, ListAllowlistIdentifiersResponse402, List['ListAllowlistIdentifiersResponse200Item']]]
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
    Union[
        ListAllowlistIdentifiersResponse401,
        ListAllowlistIdentifiersResponse402,
        List["ListAllowlistIdentifiersResponse200Item"],
    ]
]:
    """List all identifiers on the allow-list

     Get a list of all identifiers allowed to sign up to an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListAllowlistIdentifiersResponse401, ListAllowlistIdentifiersResponse402, List['ListAllowlistIdentifiersResponse200Item']]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        ListAllowlistIdentifiersResponse401,
        ListAllowlistIdentifiersResponse402,
        List["ListAllowlistIdentifiersResponse200Item"],
    ]
]:
    """List all identifiers on the allow-list

     Get a list of all identifiers allowed to sign up to an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListAllowlistIdentifiersResponse401, ListAllowlistIdentifiersResponse402, List['ListAllowlistIdentifiersResponse200Item']]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        ListAllowlistIdentifiersResponse401,
        ListAllowlistIdentifiersResponse402,
        List["ListAllowlistIdentifiersResponse200Item"],
    ]
]:
    """List all identifiers on the allow-list

     Get a list of all identifiers allowed to sign up to an instance

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListAllowlistIdentifiersResponse401, ListAllowlistIdentifiersResponse402, List['ListAllowlistIdentifiersResponse200Item']]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
