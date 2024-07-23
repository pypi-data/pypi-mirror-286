from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_saml_connections_response_200 import ListSAMLConnectionsResponse200
from ...models.list_saml_connections_response_402 import ListSAMLConnectionsResponse402
from ...models.list_saml_connections_response_403 import ListSAMLConnectionsResponse403
from ...models.list_saml_connections_response_422 import ListSAMLConnectionsResponse422
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/saml_connections",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ListSAMLConnectionsResponse200,
        ListSAMLConnectionsResponse402,
        ListSAMLConnectionsResponse403,
        ListSAMLConnectionsResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListSAMLConnectionsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = ListSAMLConnectionsResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = ListSAMLConnectionsResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ListSAMLConnectionsResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ListSAMLConnectionsResponse200,
        ListSAMLConnectionsResponse402,
        ListSAMLConnectionsResponse403,
        ListSAMLConnectionsResponse422,
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
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        ListSAMLConnectionsResponse200,
        ListSAMLConnectionsResponse402,
        ListSAMLConnectionsResponse403,
        ListSAMLConnectionsResponse422,
    ]
]:
    """Get a list of SAML Connections for an instance

     Returns the list of SAML Connections for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The SAML Connections are ordered by descending creation date and the most recent will be returned
    first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListSAMLConnectionsResponse200, ListSAMLConnectionsResponse402, ListSAMLConnectionsResponse403, ListSAMLConnectionsResponse422]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        ListSAMLConnectionsResponse200,
        ListSAMLConnectionsResponse402,
        ListSAMLConnectionsResponse403,
        ListSAMLConnectionsResponse422,
    ]
]:
    """Get a list of SAML Connections for an instance

     Returns the list of SAML Connections for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The SAML Connections are ordered by descending creation date and the most recent will be returned
    first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListSAMLConnectionsResponse200, ListSAMLConnectionsResponse402, ListSAMLConnectionsResponse403, ListSAMLConnectionsResponse422]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        ListSAMLConnectionsResponse200,
        ListSAMLConnectionsResponse402,
        ListSAMLConnectionsResponse403,
        ListSAMLConnectionsResponse422,
    ]
]:
    """Get a list of SAML Connections for an instance

     Returns the list of SAML Connections for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The SAML Connections are ordered by descending creation date and the most recent will be returned
    first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListSAMLConnectionsResponse200, ListSAMLConnectionsResponse402, ListSAMLConnectionsResponse403, ListSAMLConnectionsResponse422]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        ListSAMLConnectionsResponse200,
        ListSAMLConnectionsResponse402,
        ListSAMLConnectionsResponse403,
        ListSAMLConnectionsResponse422,
    ]
]:
    """Get a list of SAML Connections for an instance

     Returns the list of SAML Connections for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The SAML Connections are ordered by descending creation date and the most recent will be returned
    first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListSAMLConnectionsResponse200, ListSAMLConnectionsResponse402, ListSAMLConnectionsResponse403, ListSAMLConnectionsResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
