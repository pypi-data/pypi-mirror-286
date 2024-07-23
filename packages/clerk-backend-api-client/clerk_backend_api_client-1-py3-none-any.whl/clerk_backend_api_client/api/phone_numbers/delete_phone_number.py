from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_phone_number_response_200 import DeletePhoneNumberResponse200
from ...models.delete_phone_number_response_400 import DeletePhoneNumberResponse400
from ...models.delete_phone_number_response_401 import DeletePhoneNumberResponse401
from ...models.delete_phone_number_response_403 import DeletePhoneNumberResponse403
from ...models.delete_phone_number_response_404 import DeletePhoneNumberResponse404
from ...types import Response


def _get_kwargs(
    phone_number_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/phone_numbers/{phone_number_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        DeletePhoneNumberResponse200,
        DeletePhoneNumberResponse400,
        DeletePhoneNumberResponse401,
        DeletePhoneNumberResponse403,
        DeletePhoneNumberResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeletePhoneNumberResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DeletePhoneNumberResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = DeletePhoneNumberResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = DeletePhoneNumberResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeletePhoneNumberResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        DeletePhoneNumberResponse200,
        DeletePhoneNumberResponse400,
        DeletePhoneNumberResponse401,
        DeletePhoneNumberResponse403,
        DeletePhoneNumberResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        DeletePhoneNumberResponse200,
        DeletePhoneNumberResponse400,
        DeletePhoneNumberResponse401,
        DeletePhoneNumberResponse403,
        DeletePhoneNumberResponse404,
    ]
]:
    """Delete a phone number

     Delete the phone number with the given ID

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeletePhoneNumberResponse200, DeletePhoneNumberResponse400, DeletePhoneNumberResponse401, DeletePhoneNumberResponse403, DeletePhoneNumberResponse404]]
    """

    kwargs = _get_kwargs(
        phone_number_id=phone_number_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        DeletePhoneNumberResponse200,
        DeletePhoneNumberResponse400,
        DeletePhoneNumberResponse401,
        DeletePhoneNumberResponse403,
        DeletePhoneNumberResponse404,
    ]
]:
    """Delete a phone number

     Delete the phone number with the given ID

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeletePhoneNumberResponse200, DeletePhoneNumberResponse400, DeletePhoneNumberResponse401, DeletePhoneNumberResponse403, DeletePhoneNumberResponse404]
    """

    return sync_detailed(
        phone_number_id=phone_number_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        DeletePhoneNumberResponse200,
        DeletePhoneNumberResponse400,
        DeletePhoneNumberResponse401,
        DeletePhoneNumberResponse403,
        DeletePhoneNumberResponse404,
    ]
]:
    """Delete a phone number

     Delete the phone number with the given ID

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeletePhoneNumberResponse200, DeletePhoneNumberResponse400, DeletePhoneNumberResponse401, DeletePhoneNumberResponse403, DeletePhoneNumberResponse404]]
    """

    kwargs = _get_kwargs(
        phone_number_id=phone_number_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        DeletePhoneNumberResponse200,
        DeletePhoneNumberResponse400,
        DeletePhoneNumberResponse401,
        DeletePhoneNumberResponse403,
        DeletePhoneNumberResponse404,
    ]
]:
    """Delete a phone number

     Delete the phone number with the given ID

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeletePhoneNumberResponse200, DeletePhoneNumberResponse400, DeletePhoneNumberResponse401, DeletePhoneNumberResponse403, DeletePhoneNumberResponse404]
    """

    return (
        await asyncio_detailed(
            phone_number_id=phone_number_id,
            client=client,
        )
    ).parsed
