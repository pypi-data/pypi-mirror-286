from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_phone_number_body import UpdatePhoneNumberBody
from ...models.update_phone_number_response_200 import UpdatePhoneNumberResponse200
from ...models.update_phone_number_response_400 import UpdatePhoneNumberResponse400
from ...models.update_phone_number_response_401 import UpdatePhoneNumberResponse401
from ...models.update_phone_number_response_403 import UpdatePhoneNumberResponse403
from ...models.update_phone_number_response_404 import UpdatePhoneNumberResponse404
from ...types import Response


def _get_kwargs(
    phone_number_id: str,
    *,
    body: UpdatePhoneNumberBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/phone_numbers/{phone_number_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        UpdatePhoneNumberResponse200,
        UpdatePhoneNumberResponse400,
        UpdatePhoneNumberResponse401,
        UpdatePhoneNumberResponse403,
        UpdatePhoneNumberResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdatePhoneNumberResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdatePhoneNumberResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = UpdatePhoneNumberResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UpdatePhoneNumberResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdatePhoneNumberResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdatePhoneNumberResponse200,
        UpdatePhoneNumberResponse400,
        UpdatePhoneNumberResponse401,
        UpdatePhoneNumberResponse403,
        UpdatePhoneNumberResponse404,
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
    body: UpdatePhoneNumberBody,
) -> Response[
    Union[
        UpdatePhoneNumberResponse200,
        UpdatePhoneNumberResponse400,
        UpdatePhoneNumberResponse401,
        UpdatePhoneNumberResponse403,
        UpdatePhoneNumberResponse404,
    ]
]:
    """Update a phone number

     Updates a phone number

    Args:
        phone_number_id (str):
        body (UpdatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdatePhoneNumberResponse200, UpdatePhoneNumberResponse400, UpdatePhoneNumberResponse401, UpdatePhoneNumberResponse403, UpdatePhoneNumberResponse404]]
    """

    kwargs = _get_kwargs(
        phone_number_id=phone_number_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePhoneNumberBody,
) -> Optional[
    Union[
        UpdatePhoneNumberResponse200,
        UpdatePhoneNumberResponse400,
        UpdatePhoneNumberResponse401,
        UpdatePhoneNumberResponse403,
        UpdatePhoneNumberResponse404,
    ]
]:
    """Update a phone number

     Updates a phone number

    Args:
        phone_number_id (str):
        body (UpdatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdatePhoneNumberResponse200, UpdatePhoneNumberResponse400, UpdatePhoneNumberResponse401, UpdatePhoneNumberResponse403, UpdatePhoneNumberResponse404]
    """

    return sync_detailed(
        phone_number_id=phone_number_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePhoneNumberBody,
) -> Response[
    Union[
        UpdatePhoneNumberResponse200,
        UpdatePhoneNumberResponse400,
        UpdatePhoneNumberResponse401,
        UpdatePhoneNumberResponse403,
        UpdatePhoneNumberResponse404,
    ]
]:
    """Update a phone number

     Updates a phone number

    Args:
        phone_number_id (str):
        body (UpdatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdatePhoneNumberResponse200, UpdatePhoneNumberResponse400, UpdatePhoneNumberResponse401, UpdatePhoneNumberResponse403, UpdatePhoneNumberResponse404]]
    """

    kwargs = _get_kwargs(
        phone_number_id=phone_number_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    phone_number_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdatePhoneNumberBody,
) -> Optional[
    Union[
        UpdatePhoneNumberResponse200,
        UpdatePhoneNumberResponse400,
        UpdatePhoneNumberResponse401,
        UpdatePhoneNumberResponse403,
        UpdatePhoneNumberResponse404,
    ]
]:
    """Update a phone number

     Updates a phone number

    Args:
        phone_number_id (str):
        body (UpdatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdatePhoneNumberResponse200, UpdatePhoneNumberResponse400, UpdatePhoneNumberResponse401, UpdatePhoneNumberResponse403, UpdatePhoneNumberResponse404]
    """

    return (
        await asyncio_detailed(
            phone_number_id=phone_number_id,
            client=client,
            body=body,
        )
    ).parsed
