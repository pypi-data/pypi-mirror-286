from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_email_address_response_200 import DeleteEmailAddressResponse200
from ...models.delete_email_address_response_400 import DeleteEmailAddressResponse400
from ...models.delete_email_address_response_401 import DeleteEmailAddressResponse401
from ...models.delete_email_address_response_403 import DeleteEmailAddressResponse403
from ...models.delete_email_address_response_404 import DeleteEmailAddressResponse404
from ...types import Response


def _get_kwargs(
    email_address_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/email_addresses/{email_address_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DeleteEmailAddressResponse200,
        DeleteEmailAddressResponse400,
        DeleteEmailAddressResponse401,
        DeleteEmailAddressResponse403,
        DeleteEmailAddressResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteEmailAddressResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DeleteEmailAddressResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = DeleteEmailAddressResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = DeleteEmailAddressResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteEmailAddressResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DeleteEmailAddressResponse200,
        DeleteEmailAddressResponse400,
        DeleteEmailAddressResponse401,
        DeleteEmailAddressResponse403,
        DeleteEmailAddressResponse404,
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
        DeleteEmailAddressResponse200,
        DeleteEmailAddressResponse400,
        DeleteEmailAddressResponse401,
        DeleteEmailAddressResponse403,
        DeleteEmailAddressResponse404,
    ]
]:
    """Delete an email address

     Delete the email address with the given ID

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteEmailAddressResponse200, DeleteEmailAddressResponse400, DeleteEmailAddressResponse401, DeleteEmailAddressResponse403, DeleteEmailAddressResponse404]]
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
        DeleteEmailAddressResponse200,
        DeleteEmailAddressResponse400,
        DeleteEmailAddressResponse401,
        DeleteEmailAddressResponse403,
        DeleteEmailAddressResponse404,
    ]
]:
    """Delete an email address

     Delete the email address with the given ID

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteEmailAddressResponse200, DeleteEmailAddressResponse400, DeleteEmailAddressResponse401, DeleteEmailAddressResponse403, DeleteEmailAddressResponse404]
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
        DeleteEmailAddressResponse200,
        DeleteEmailAddressResponse400,
        DeleteEmailAddressResponse401,
        DeleteEmailAddressResponse403,
        DeleteEmailAddressResponse404,
    ]
]:
    """Delete an email address

     Delete the email address with the given ID

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteEmailAddressResponse200, DeleteEmailAddressResponse400, DeleteEmailAddressResponse401, DeleteEmailAddressResponse403, DeleteEmailAddressResponse404]]
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
        DeleteEmailAddressResponse200,
        DeleteEmailAddressResponse400,
        DeleteEmailAddressResponse401,
        DeleteEmailAddressResponse403,
        DeleteEmailAddressResponse404,
    ]
]:
    """Delete an email address

     Delete the email address with the given ID

    Args:
        email_address_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteEmailAddressResponse200, DeleteEmailAddressResponse400, DeleteEmailAddressResponse401, DeleteEmailAddressResponse403, DeleteEmailAddressResponse404]
    """

    return (
        await asyncio_detailed(
            email_address_id=email_address_id,
            client=client,
        )
    ).parsed
