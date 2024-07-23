from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_email_address_body import UpdateEmailAddressBody
from ...models.update_email_address_response_200 import UpdateEmailAddressResponse200
from ...models.update_email_address_response_400 import UpdateEmailAddressResponse400
from ...models.update_email_address_response_401 import UpdateEmailAddressResponse401
from ...models.update_email_address_response_403 import UpdateEmailAddressResponse403
from ...models.update_email_address_response_404 import UpdateEmailAddressResponse404
from ...types import Response


def _get_kwargs(
    email_address_id: str,
    *,
    body: UpdateEmailAddressBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/email_addresses/{email_address_id}",
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
        UpdateEmailAddressResponse200,
        UpdateEmailAddressResponse400,
        UpdateEmailAddressResponse401,
        UpdateEmailAddressResponse403,
        UpdateEmailAddressResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateEmailAddressResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateEmailAddressResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = UpdateEmailAddressResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UpdateEmailAddressResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateEmailAddressResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateEmailAddressResponse200,
        UpdateEmailAddressResponse400,
        UpdateEmailAddressResponse401,
        UpdateEmailAddressResponse403,
        UpdateEmailAddressResponse404,
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
    body: UpdateEmailAddressBody,
) -> Response[
    Union[
        UpdateEmailAddressResponse200,
        UpdateEmailAddressResponse400,
        UpdateEmailAddressResponse401,
        UpdateEmailAddressResponse403,
        UpdateEmailAddressResponse404,
    ]
]:
    """Update an email address

     Updates an email address.

    Args:
        email_address_id (str):
        body (UpdateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateEmailAddressResponse200, UpdateEmailAddressResponse400, UpdateEmailAddressResponse401, UpdateEmailAddressResponse403, UpdateEmailAddressResponse404]]
    """

    kwargs = _get_kwargs(
        email_address_id=email_address_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateEmailAddressBody,
) -> Optional[
    Union[
        UpdateEmailAddressResponse200,
        UpdateEmailAddressResponse400,
        UpdateEmailAddressResponse401,
        UpdateEmailAddressResponse403,
        UpdateEmailAddressResponse404,
    ]
]:
    """Update an email address

     Updates an email address.

    Args:
        email_address_id (str):
        body (UpdateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateEmailAddressResponse200, UpdateEmailAddressResponse400, UpdateEmailAddressResponse401, UpdateEmailAddressResponse403, UpdateEmailAddressResponse404]
    """

    return sync_detailed(
        email_address_id=email_address_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateEmailAddressBody,
) -> Response[
    Union[
        UpdateEmailAddressResponse200,
        UpdateEmailAddressResponse400,
        UpdateEmailAddressResponse401,
        UpdateEmailAddressResponse403,
        UpdateEmailAddressResponse404,
    ]
]:
    """Update an email address

     Updates an email address.

    Args:
        email_address_id (str):
        body (UpdateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateEmailAddressResponse200, UpdateEmailAddressResponse400, UpdateEmailAddressResponse401, UpdateEmailAddressResponse403, UpdateEmailAddressResponse404]]
    """

    kwargs = _get_kwargs(
        email_address_id=email_address_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email_address_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateEmailAddressBody,
) -> Optional[
    Union[
        UpdateEmailAddressResponse200,
        UpdateEmailAddressResponse400,
        UpdateEmailAddressResponse401,
        UpdateEmailAddressResponse403,
        UpdateEmailAddressResponse404,
    ]
]:
    """Update an email address

     Updates an email address.

    Args:
        email_address_id (str):
        body (UpdateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateEmailAddressResponse200, UpdateEmailAddressResponse400, UpdateEmailAddressResponse401, UpdateEmailAddressResponse403, UpdateEmailAddressResponse404]
    """

    return (
        await asyncio_detailed(
            email_address_id=email_address_id,
            client=client,
            body=body,
        )
    ).parsed
