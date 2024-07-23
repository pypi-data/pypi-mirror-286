from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_blocklist_identifier_response_200 import DeleteBlocklistIdentifierResponse200
from ...models.delete_blocklist_identifier_response_402 import DeleteBlocklistIdentifierResponse402
from ...models.delete_blocklist_identifier_response_404 import DeleteBlocklistIdentifierResponse404
from ...types import Response


def _get_kwargs(
    identifier_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/blocklist_identifiers/{identifier_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteBlocklistIdentifierResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = DeleteBlocklistIdentifierResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteBlocklistIdentifierResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404
    ]
]:
    """Delete identifier from block-list

     Delete an identifier from the instance block-list

    Args:
        identifier_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404]]
    """

    kwargs = _get_kwargs(
        identifier_id=identifier_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404
    ]
]:
    """Delete identifier from block-list

     Delete an identifier from the instance block-list

    Args:
        identifier_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404]
    """

    return sync_detailed(
        identifier_id=identifier_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    identifier_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404
    ]
]:
    """Delete identifier from block-list

     Delete an identifier from the instance block-list

    Args:
        identifier_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404]]
    """

    kwargs = _get_kwargs(
        identifier_id=identifier_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404
    ]
]:
    """Delete identifier from block-list

     Delete an identifier from the instance block-list

    Args:
        identifier_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteBlocklistIdentifierResponse200, DeleteBlocklistIdentifierResponse402, DeleteBlocklistIdentifierResponse404]
    """

    return (
        await asyncio_detailed(
            identifier_id=identifier_id,
            client=client,
        )
    ).parsed
