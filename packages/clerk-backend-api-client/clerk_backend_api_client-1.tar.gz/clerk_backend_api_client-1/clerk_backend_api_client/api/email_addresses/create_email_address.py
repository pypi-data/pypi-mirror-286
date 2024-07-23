from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_email_address_body import CreateEmailAddressBody
from ...models.create_email_address_response_200 import CreateEmailAddressResponse200
from ...models.create_email_address_response_400 import CreateEmailAddressResponse400
from ...models.create_email_address_response_401 import CreateEmailAddressResponse401
from ...models.create_email_address_response_403 import CreateEmailAddressResponse403
from ...models.create_email_address_response_404 import CreateEmailAddressResponse404
from ...models.create_email_address_response_422 import CreateEmailAddressResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateEmailAddressBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/email_addresses",
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
        CreateEmailAddressResponse200,
        CreateEmailAddressResponse400,
        CreateEmailAddressResponse401,
        CreateEmailAddressResponse403,
        CreateEmailAddressResponse404,
        CreateEmailAddressResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateEmailAddressResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateEmailAddressResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = CreateEmailAddressResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreateEmailAddressResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateEmailAddressResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateEmailAddressResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateEmailAddressResponse200,
        CreateEmailAddressResponse400,
        CreateEmailAddressResponse401,
        CreateEmailAddressResponse403,
        CreateEmailAddressResponse404,
        CreateEmailAddressResponse422,
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
    body: CreateEmailAddressBody,
) -> Response[
    Union[
        CreateEmailAddressResponse200,
        CreateEmailAddressResponse400,
        CreateEmailAddressResponse401,
        CreateEmailAddressResponse403,
        CreateEmailAddressResponse404,
        CreateEmailAddressResponse422,
    ]
]:
    """Create an email address

     Create a new email address

    Args:
        body (CreateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateEmailAddressResponse200, CreateEmailAddressResponse400, CreateEmailAddressResponse401, CreateEmailAddressResponse403, CreateEmailAddressResponse404, CreateEmailAddressResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateEmailAddressBody,
) -> Optional[
    Union[
        CreateEmailAddressResponse200,
        CreateEmailAddressResponse400,
        CreateEmailAddressResponse401,
        CreateEmailAddressResponse403,
        CreateEmailAddressResponse404,
        CreateEmailAddressResponse422,
    ]
]:
    """Create an email address

     Create a new email address

    Args:
        body (CreateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateEmailAddressResponse200, CreateEmailAddressResponse400, CreateEmailAddressResponse401, CreateEmailAddressResponse403, CreateEmailAddressResponse404, CreateEmailAddressResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateEmailAddressBody,
) -> Response[
    Union[
        CreateEmailAddressResponse200,
        CreateEmailAddressResponse400,
        CreateEmailAddressResponse401,
        CreateEmailAddressResponse403,
        CreateEmailAddressResponse404,
        CreateEmailAddressResponse422,
    ]
]:
    """Create an email address

     Create a new email address

    Args:
        body (CreateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateEmailAddressResponse200, CreateEmailAddressResponse400, CreateEmailAddressResponse401, CreateEmailAddressResponse403, CreateEmailAddressResponse404, CreateEmailAddressResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateEmailAddressBody,
) -> Optional[
    Union[
        CreateEmailAddressResponse200,
        CreateEmailAddressResponse400,
        CreateEmailAddressResponse401,
        CreateEmailAddressResponse403,
        CreateEmailAddressResponse404,
        CreateEmailAddressResponse422,
    ]
]:
    """Create an email address

     Create a new email address

    Args:
        body (CreateEmailAddressBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateEmailAddressResponse200, CreateEmailAddressResponse400, CreateEmailAddressResponse401, CreateEmailAddressResponse403, CreateEmailAddressResponse404, CreateEmailAddressResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
