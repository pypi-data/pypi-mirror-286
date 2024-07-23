from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_o_auth_application_body import CreateOAuthApplicationBody
from ...models.create_o_auth_application_response_200 import CreateOAuthApplicationResponse200
from ...models.create_o_auth_application_response_400 import CreateOAuthApplicationResponse400
from ...models.create_o_auth_application_response_403 import CreateOAuthApplicationResponse403
from ...models.create_o_auth_application_response_422 import CreateOAuthApplicationResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateOAuthApplicationBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/oauth_applications",
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
        CreateOAuthApplicationResponse200,
        CreateOAuthApplicationResponse400,
        CreateOAuthApplicationResponse403,
        CreateOAuthApplicationResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateOAuthApplicationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateOAuthApplicationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreateOAuthApplicationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateOAuthApplicationResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateOAuthApplicationResponse200,
        CreateOAuthApplicationResponse400,
        CreateOAuthApplicationResponse403,
        CreateOAuthApplicationResponse422,
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
    body: CreateOAuthApplicationBody,
) -> Response[
    Union[
        CreateOAuthApplicationResponse200,
        CreateOAuthApplicationResponse400,
        CreateOAuthApplicationResponse403,
        CreateOAuthApplicationResponse422,
    ]
]:
    """Create an OAuth application

     Creates a new OAuth application with the given name and callback URL for an instance.
    The callback URL must be a valid url.
    All URL schemes are allowed such as `http://`, `https://`, `myapp://`, etc...

    Args:
        body (CreateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOAuthApplicationResponse200, CreateOAuthApplicationResponse400, CreateOAuthApplicationResponse403, CreateOAuthApplicationResponse422]]
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
    body: CreateOAuthApplicationBody,
) -> Optional[
    Union[
        CreateOAuthApplicationResponse200,
        CreateOAuthApplicationResponse400,
        CreateOAuthApplicationResponse403,
        CreateOAuthApplicationResponse422,
    ]
]:
    """Create an OAuth application

     Creates a new OAuth application with the given name and callback URL for an instance.
    The callback URL must be a valid url.
    All URL schemes are allowed such as `http://`, `https://`, `myapp://`, etc...

    Args:
        body (CreateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOAuthApplicationResponse200, CreateOAuthApplicationResponse400, CreateOAuthApplicationResponse403, CreateOAuthApplicationResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOAuthApplicationBody,
) -> Response[
    Union[
        CreateOAuthApplicationResponse200,
        CreateOAuthApplicationResponse400,
        CreateOAuthApplicationResponse403,
        CreateOAuthApplicationResponse422,
    ]
]:
    """Create an OAuth application

     Creates a new OAuth application with the given name and callback URL for an instance.
    The callback URL must be a valid url.
    All URL schemes are allowed such as `http://`, `https://`, `myapp://`, etc...

    Args:
        body (CreateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOAuthApplicationResponse200, CreateOAuthApplicationResponse400, CreateOAuthApplicationResponse403, CreateOAuthApplicationResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOAuthApplicationBody,
) -> Optional[
    Union[
        CreateOAuthApplicationResponse200,
        CreateOAuthApplicationResponse400,
        CreateOAuthApplicationResponse403,
        CreateOAuthApplicationResponse422,
    ]
]:
    """Create an OAuth application

     Creates a new OAuth application with the given name and callback URL for an instance.
    The callback URL must be a valid url.
    All URL schemes are allowed such as `http://`, `https://`, `myapp://`, etc...

    Args:
        body (CreateOAuthApplicationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOAuthApplicationResponse200, CreateOAuthApplicationResponse400, CreateOAuthApplicationResponse403, CreateOAuthApplicationResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
