from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_saml_connection_response_200 import GetSAMLConnectionResponse200
from ...models.get_saml_connection_response_402 import GetSAMLConnectionResponse402
from ...models.get_saml_connection_response_403 import GetSAMLConnectionResponse403
from ...models.get_saml_connection_response_404 import GetSAMLConnectionResponse404
from ...types import Response


def _get_kwargs(
    saml_connection_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/saml_connections/{saml_connection_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetSAMLConnectionResponse200,
        GetSAMLConnectionResponse402,
        GetSAMLConnectionResponse403,
        GetSAMLConnectionResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetSAMLConnectionResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = GetSAMLConnectionResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = GetSAMLConnectionResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetSAMLConnectionResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetSAMLConnectionResponse200,
        GetSAMLConnectionResponse402,
        GetSAMLConnectionResponse403,
        GetSAMLConnectionResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetSAMLConnectionResponse200,
        GetSAMLConnectionResponse402,
        GetSAMLConnectionResponse403,
        GetSAMLConnectionResponse404,
    ]
]:
    """Retrieve a SAML Connection by ID

     Fetches the SAML Connection whose ID matches the provided `saml_connection_id` in the path.

    Args:
        saml_connection_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSAMLConnectionResponse200, GetSAMLConnectionResponse402, GetSAMLConnectionResponse403, GetSAMLConnectionResponse404]]
    """

    kwargs = _get_kwargs(
        saml_connection_id=saml_connection_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetSAMLConnectionResponse200,
        GetSAMLConnectionResponse402,
        GetSAMLConnectionResponse403,
        GetSAMLConnectionResponse404,
    ]
]:
    """Retrieve a SAML Connection by ID

     Fetches the SAML Connection whose ID matches the provided `saml_connection_id` in the path.

    Args:
        saml_connection_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSAMLConnectionResponse200, GetSAMLConnectionResponse402, GetSAMLConnectionResponse403, GetSAMLConnectionResponse404]
    """

    return sync_detailed(
        saml_connection_id=saml_connection_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetSAMLConnectionResponse200,
        GetSAMLConnectionResponse402,
        GetSAMLConnectionResponse403,
        GetSAMLConnectionResponse404,
    ]
]:
    """Retrieve a SAML Connection by ID

     Fetches the SAML Connection whose ID matches the provided `saml_connection_id` in the path.

    Args:
        saml_connection_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSAMLConnectionResponse200, GetSAMLConnectionResponse402, GetSAMLConnectionResponse403, GetSAMLConnectionResponse404]]
    """

    kwargs = _get_kwargs(
        saml_connection_id=saml_connection_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetSAMLConnectionResponse200,
        GetSAMLConnectionResponse402,
        GetSAMLConnectionResponse403,
        GetSAMLConnectionResponse404,
    ]
]:
    """Retrieve a SAML Connection by ID

     Fetches the SAML Connection whose ID matches the provided `saml_connection_id` in the path.

    Args:
        saml_connection_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSAMLConnectionResponse200, GetSAMLConnectionResponse402, GetSAMLConnectionResponse403, GetSAMLConnectionResponse404]
    """

    return (
        await asyncio_detailed(
            saml_connection_id=saml_connection_id,
            client=client,
        )
    ).parsed
