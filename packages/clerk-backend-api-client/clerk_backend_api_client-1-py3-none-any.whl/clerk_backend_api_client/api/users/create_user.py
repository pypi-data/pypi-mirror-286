from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_user_body import CreateUserBody
from ...models.create_user_response_200 import CreateUserResponse200
from ...models.create_user_response_400 import CreateUserResponse400
from ...models.create_user_response_401 import CreateUserResponse401
from ...models.create_user_response_403 import CreateUserResponse403
from ...models.create_user_response_422 import CreateUserResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateUserBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/users",
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
        CreateUserResponse200,
        CreateUserResponse400,
        CreateUserResponse401,
        CreateUserResponse403,
        CreateUserResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateUserResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateUserResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = CreateUserResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreateUserResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateUserResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateUserResponse200,
        CreateUserResponse400,
        CreateUserResponse401,
        CreateUserResponse403,
        CreateUserResponse422,
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
    body: CreateUserBody,
) -> Response[
    Union[
        CreateUserResponse200,
        CreateUserResponse400,
        CreateUserResponse401,
        CreateUserResponse403,
        CreateUserResponse422,
    ]
]:
    """Create a new user

     Creates a new user. Your user management settings determine how you should setup your user model.

    Any email address and phone number created using this method will be marked as verified.

    Note: If you are performing a migration, check out our guide on [zero downtime
    migrations](https://clerk.com/docs/deployments/migrate-overview).

    A rate limit rule of 20 requests per 10 seconds is applied to this endpoint.

    Args:
        body (CreateUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUserResponse200, CreateUserResponse400, CreateUserResponse401, CreateUserResponse403, CreateUserResponse422]]
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
    body: CreateUserBody,
) -> Optional[
    Union[
        CreateUserResponse200,
        CreateUserResponse400,
        CreateUserResponse401,
        CreateUserResponse403,
        CreateUserResponse422,
    ]
]:
    """Create a new user

     Creates a new user. Your user management settings determine how you should setup your user model.

    Any email address and phone number created using this method will be marked as verified.

    Note: If you are performing a migration, check out our guide on [zero downtime
    migrations](https://clerk.com/docs/deployments/migrate-overview).

    A rate limit rule of 20 requests per 10 seconds is applied to this endpoint.

    Args:
        body (CreateUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUserResponse200, CreateUserResponse400, CreateUserResponse401, CreateUserResponse403, CreateUserResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateUserBody,
) -> Response[
    Union[
        CreateUserResponse200,
        CreateUserResponse400,
        CreateUserResponse401,
        CreateUserResponse403,
        CreateUserResponse422,
    ]
]:
    """Create a new user

     Creates a new user. Your user management settings determine how you should setup your user model.

    Any email address and phone number created using this method will be marked as verified.

    Note: If you are performing a migration, check out our guide on [zero downtime
    migrations](https://clerk.com/docs/deployments/migrate-overview).

    A rate limit rule of 20 requests per 10 seconds is applied to this endpoint.

    Args:
        body (CreateUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUserResponse200, CreateUserResponse400, CreateUserResponse401, CreateUserResponse403, CreateUserResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateUserBody,
) -> Optional[
    Union[
        CreateUserResponse200,
        CreateUserResponse400,
        CreateUserResponse401,
        CreateUserResponse403,
        CreateUserResponse422,
    ]
]:
    """Create a new user

     Creates a new user. Your user management settings determine how you should setup your user model.

    Any email address and phone number created using this method will be marked as verified.

    Note: If you are performing a migration, check out our guide on [zero downtime
    migrations](https://clerk.com/docs/deployments/migrate-overview).

    A rate limit rule of 20 requests per 10 seconds is applied to this endpoint.

    Args:
        body (CreateUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUserResponse200, CreateUserResponse400, CreateUserResponse401, CreateUserResponse403, CreateUserResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
