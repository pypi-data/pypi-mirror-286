from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_email_address_response_200 import GetEmailAddressResponse200
from ...models.get_email_address_response_400 import GetEmailAddressResponse400
from ...models.get_email_address_response_401 import GetEmailAddressResponse401
from ...models.get_email_address_response_403 import GetEmailAddressResponse403
from ...models.get_email_address_response_404 import GetEmailAddressResponse404
from ...types import Response


def _get_kwargs(
    email_address_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/email_addresses/{email_address_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetEmailAddressResponse200,
        GetEmailAddressResponse400,
        GetEmailAddressResponse401,
        GetEmailAddressResponse403,
        GetEmailAddressResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetEmailAddressResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetEmailAddressResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetEmailAddressResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = GetEmailAddressResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetEmailAddressResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetEmailAddressResponse200,
        GetEmailAddressResponse400,
        GetEmailAddressResponse401,
        GetEmailAddressResponse403,
        GetEmailAddressResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetEmailAddressResponse200,
        GetEmailAddressResponse400,
        GetEmailAddressResponse401,
        GetEmailAddressResponse403,
        GetEmailAddressResponse404,
    ]
]:
    """Retrieve an email address

     Returns the details of an email address.

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEmailAddressResponse200, GetEmailAddressResponse400, GetEmailAddressResponse401, GetEmailAddressResponse403, GetEmailAddressResponse404]]
    """

    kwargs = _get_kwargs(
        email_address_id=email_address_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetEmailAddressResponse200,
        GetEmailAddressResponse400,
        GetEmailAddressResponse401,
        GetEmailAddressResponse403,
        GetEmailAddressResponse404,
    ]
]:
    """Retrieve an email address

     Returns the details of an email address.

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEmailAddressResponse200, GetEmailAddressResponse400, GetEmailAddressResponse401, GetEmailAddressResponse403, GetEmailAddressResponse404]
    """

    return sync_detailed(
        email_address_id=email_address_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetEmailAddressResponse200,
        GetEmailAddressResponse400,
        GetEmailAddressResponse401,
        GetEmailAddressResponse403,
        GetEmailAddressResponse404,
    ]
]:
    """Retrieve an email address

     Returns the details of an email address.

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetEmailAddressResponse200, GetEmailAddressResponse400, GetEmailAddressResponse401, GetEmailAddressResponse403, GetEmailAddressResponse404]]
    """

    kwargs = _get_kwargs(
        email_address_id=email_address_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetEmailAddressResponse200,
        GetEmailAddressResponse400,
        GetEmailAddressResponse401,
        GetEmailAddressResponse403,
        GetEmailAddressResponse404,
    ]
]:
    """Retrieve an email address

     Returns the details of an email address.

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetEmailAddressResponse200, GetEmailAddressResponse400, GetEmailAddressResponse401, GetEmailAddressResponse403, GetEmailAddressResponse404]
    """

    return (
        await asyncio_detailed(
            email_address_id=email_address_id,
            client=client,
        )
    ).parsed
