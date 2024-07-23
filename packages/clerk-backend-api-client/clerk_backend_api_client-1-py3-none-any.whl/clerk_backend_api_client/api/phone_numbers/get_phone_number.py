from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_phone_number_response_200 import GetPhoneNumberResponse200
from ...models.get_phone_number_response_400 import GetPhoneNumberResponse400
from ...models.get_phone_number_response_401 import GetPhoneNumberResponse401
from ...models.get_phone_number_response_403 import GetPhoneNumberResponse403
from ...models.get_phone_number_response_404 import GetPhoneNumberResponse404
from ...types import Response


def _get_kwargs(
    phone_number_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/phone_numbers/{phone_number_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetPhoneNumberResponse200,
        GetPhoneNumberResponse400,
        GetPhoneNumberResponse401,
        GetPhoneNumberResponse403,
        GetPhoneNumberResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetPhoneNumberResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetPhoneNumberResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetPhoneNumberResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = GetPhoneNumberResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetPhoneNumberResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetPhoneNumberResponse200,
        GetPhoneNumberResponse400,
        GetPhoneNumberResponse401,
        GetPhoneNumberResponse403,
        GetPhoneNumberResponse404,
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
        GetPhoneNumberResponse200,
        GetPhoneNumberResponse400,
        GetPhoneNumberResponse401,
        GetPhoneNumberResponse403,
        GetPhoneNumberResponse404,
    ]
]:
    """Retrieve a phone number

     Returns the details of a phone number

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPhoneNumberResponse200, GetPhoneNumberResponse400, GetPhoneNumberResponse401, GetPhoneNumberResponse403, GetPhoneNumberResponse404]]
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
        GetPhoneNumberResponse200,
        GetPhoneNumberResponse400,
        GetPhoneNumberResponse401,
        GetPhoneNumberResponse403,
        GetPhoneNumberResponse404,
    ]
]:
    """Retrieve a phone number

     Returns the details of a phone number

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPhoneNumberResponse200, GetPhoneNumberResponse400, GetPhoneNumberResponse401, GetPhoneNumberResponse403, GetPhoneNumberResponse404]
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
        GetPhoneNumberResponse200,
        GetPhoneNumberResponse400,
        GetPhoneNumberResponse401,
        GetPhoneNumberResponse403,
        GetPhoneNumberResponse404,
    ]
]:
    """Retrieve a phone number

     Returns the details of a phone number

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPhoneNumberResponse200, GetPhoneNumberResponse400, GetPhoneNumberResponse401, GetPhoneNumberResponse403, GetPhoneNumberResponse404]]
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
        GetPhoneNumberResponse200,
        GetPhoneNumberResponse400,
        GetPhoneNumberResponse401,
        GetPhoneNumberResponse403,
        GetPhoneNumberResponse404,
    ]
]:
    """Retrieve a phone number

     Returns the details of a phone number

    Args:
        phone_number_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPhoneNumberResponse200, GetPhoneNumberResponse400, GetPhoneNumberResponse401, GetPhoneNumberResponse403, GetPhoneNumberResponse404]
    """

    return (
        await asyncio_detailed(
            phone_number_id=phone_number_id,
            client=client,
        )
    ).parsed
