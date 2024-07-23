from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_phone_number_body import CreatePhoneNumberBody
from ...models.create_phone_number_response_200 import CreatePhoneNumberResponse200
from ...models.create_phone_number_response_400 import CreatePhoneNumberResponse400
from ...models.create_phone_number_response_401 import CreatePhoneNumberResponse401
from ...models.create_phone_number_response_403 import CreatePhoneNumberResponse403
from ...models.create_phone_number_response_404 import CreatePhoneNumberResponse404
from ...models.create_phone_number_response_422 import CreatePhoneNumberResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreatePhoneNumberBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/phone_numbers",
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
        CreatePhoneNumberResponse200,
        CreatePhoneNumberResponse400,
        CreatePhoneNumberResponse401,
        CreatePhoneNumberResponse403,
        CreatePhoneNumberResponse404,
        CreatePhoneNumberResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreatePhoneNumberResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreatePhoneNumberResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = CreatePhoneNumberResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreatePhoneNumberResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreatePhoneNumberResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreatePhoneNumberResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreatePhoneNumberResponse200,
        CreatePhoneNumberResponse400,
        CreatePhoneNumberResponse401,
        CreatePhoneNumberResponse403,
        CreatePhoneNumberResponse404,
        CreatePhoneNumberResponse422,
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
    body: CreatePhoneNumberBody,
) -> Response[
    Union[
        CreatePhoneNumberResponse200,
        CreatePhoneNumberResponse400,
        CreatePhoneNumberResponse401,
        CreatePhoneNumberResponse403,
        CreatePhoneNumberResponse404,
        CreatePhoneNumberResponse422,
    ]
]:
    """Create a phone number

     Create a new phone number

    Args:
        body (CreatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreatePhoneNumberResponse200, CreatePhoneNumberResponse400, CreatePhoneNumberResponse401, CreatePhoneNumberResponse403, CreatePhoneNumberResponse404, CreatePhoneNumberResponse422]]
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
    body: CreatePhoneNumberBody,
) -> Optional[
    Union[
        CreatePhoneNumberResponse200,
        CreatePhoneNumberResponse400,
        CreatePhoneNumberResponse401,
        CreatePhoneNumberResponse403,
        CreatePhoneNumberResponse404,
        CreatePhoneNumberResponse422,
    ]
]:
    """Create a phone number

     Create a new phone number

    Args:
        body (CreatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreatePhoneNumberResponse200, CreatePhoneNumberResponse400, CreatePhoneNumberResponse401, CreatePhoneNumberResponse403, CreatePhoneNumberResponse404, CreatePhoneNumberResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreatePhoneNumberBody,
) -> Response[
    Union[
        CreatePhoneNumberResponse200,
        CreatePhoneNumberResponse400,
        CreatePhoneNumberResponse401,
        CreatePhoneNumberResponse403,
        CreatePhoneNumberResponse404,
        CreatePhoneNumberResponse422,
    ]
]:
    """Create a phone number

     Create a new phone number

    Args:
        body (CreatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreatePhoneNumberResponse200, CreatePhoneNumberResponse400, CreatePhoneNumberResponse401, CreatePhoneNumberResponse403, CreatePhoneNumberResponse404, CreatePhoneNumberResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreatePhoneNumberBody,
) -> Optional[
    Union[
        CreatePhoneNumberResponse200,
        CreatePhoneNumberResponse400,
        CreatePhoneNumberResponse401,
        CreatePhoneNumberResponse403,
        CreatePhoneNumberResponse404,
        CreatePhoneNumberResponse422,
    ]
]:
    """Create a phone number

     Create a new phone number

    Args:
        body (CreatePhoneNumberBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreatePhoneNumberResponse200, CreatePhoneNumberResponse400, CreatePhoneNumberResponse401, CreatePhoneNumberResponse403, CreatePhoneNumberResponse404, CreatePhoneNumberResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
