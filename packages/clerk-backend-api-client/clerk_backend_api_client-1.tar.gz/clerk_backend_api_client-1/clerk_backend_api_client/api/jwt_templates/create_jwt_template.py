from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_jwt_template_body import CreateJWTTemplateBody
from ...models.create_jwt_template_response_200 import CreateJWTTemplateResponse200
from ...models.create_jwt_template_response_400 import CreateJWTTemplateResponse400
from ...models.create_jwt_template_response_402 import CreateJWTTemplateResponse402
from ...models.create_jwt_template_response_422 import CreateJWTTemplateResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateJWTTemplateBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/jwt_templates",
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
        CreateJWTTemplateResponse200,
        CreateJWTTemplateResponse400,
        CreateJWTTemplateResponse402,
        CreateJWTTemplateResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateJWTTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateJWTTemplateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = CreateJWTTemplateResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateJWTTemplateResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateJWTTemplateResponse200,
        CreateJWTTemplateResponse400,
        CreateJWTTemplateResponse402,
        CreateJWTTemplateResponse422,
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
    body: CreateJWTTemplateBody,
) -> Response[
    Union[
        CreateJWTTemplateResponse200,
        CreateJWTTemplateResponse400,
        CreateJWTTemplateResponse402,
        CreateJWTTemplateResponse422,
    ]
]:
    """Create a JWT template

     Create a new JWT template

    Args:
        body (CreateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateJWTTemplateResponse200, CreateJWTTemplateResponse400, CreateJWTTemplateResponse402, CreateJWTTemplateResponse422]]
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
    body: CreateJWTTemplateBody,
) -> Optional[
    Union[
        CreateJWTTemplateResponse200,
        CreateJWTTemplateResponse400,
        CreateJWTTemplateResponse402,
        CreateJWTTemplateResponse422,
    ]
]:
    """Create a JWT template

     Create a new JWT template

    Args:
        body (CreateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateJWTTemplateResponse200, CreateJWTTemplateResponse400, CreateJWTTemplateResponse402, CreateJWTTemplateResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateJWTTemplateBody,
) -> Response[
    Union[
        CreateJWTTemplateResponse200,
        CreateJWTTemplateResponse400,
        CreateJWTTemplateResponse402,
        CreateJWTTemplateResponse422,
    ]
]:
    """Create a JWT template

     Create a new JWT template

    Args:
        body (CreateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateJWTTemplateResponse200, CreateJWTTemplateResponse400, CreateJWTTemplateResponse402, CreateJWTTemplateResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateJWTTemplateBody,
) -> Optional[
    Union[
        CreateJWTTemplateResponse200,
        CreateJWTTemplateResponse400,
        CreateJWTTemplateResponse402,
        CreateJWTTemplateResponse422,
    ]
]:
    """Create a JWT template

     Create a new JWT template

    Args:
        body (CreateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateJWTTemplateResponse200, CreateJWTTemplateResponse400, CreateJWTTemplateResponse402, CreateJWTTemplateResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
