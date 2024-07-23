from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_blocklist_identifier_body import CreateBlocklistIdentifierBody
from ...models.create_blocklist_identifier_response_200 import CreateBlocklistIdentifierResponse200
from ...models.create_blocklist_identifier_response_400 import CreateBlocklistIdentifierResponse400
from ...models.create_blocklist_identifier_response_402 import CreateBlocklistIdentifierResponse402
from ...models.create_blocklist_identifier_response_422 import CreateBlocklistIdentifierResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateBlocklistIdentifierBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/blocklist_identifiers",
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
        CreateBlocklistIdentifierResponse200,
        CreateBlocklistIdentifierResponse400,
        CreateBlocklistIdentifierResponse402,
        CreateBlocklistIdentifierResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateBlocklistIdentifierResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateBlocklistIdentifierResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = CreateBlocklistIdentifierResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateBlocklistIdentifierResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateBlocklistIdentifierResponse200,
        CreateBlocklistIdentifierResponse400,
        CreateBlocklistIdentifierResponse402,
        CreateBlocklistIdentifierResponse422,
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
    body: CreateBlocklistIdentifierBody,
) -> Response[
    Union[
        CreateBlocklistIdentifierResponse200,
        CreateBlocklistIdentifierResponse400,
        CreateBlocklistIdentifierResponse402,
        CreateBlocklistIdentifierResponse422,
    ]
]:
    """Add identifier to the block-list

     Create an identifier that is blocked from accessing an instance

    Args:
        body (CreateBlocklistIdentifierBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBlocklistIdentifierResponse200, CreateBlocklistIdentifierResponse400, CreateBlocklistIdentifierResponse402, CreateBlocklistIdentifierResponse422]]
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
    body: CreateBlocklistIdentifierBody,
) -> Optional[
    Union[
        CreateBlocklistIdentifierResponse200,
        CreateBlocklistIdentifierResponse400,
        CreateBlocklistIdentifierResponse402,
        CreateBlocklistIdentifierResponse422,
    ]
]:
    """Add identifier to the block-list

     Create an identifier that is blocked from accessing an instance

    Args:
        body (CreateBlocklistIdentifierBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBlocklistIdentifierResponse200, CreateBlocklistIdentifierResponse400, CreateBlocklistIdentifierResponse402, CreateBlocklistIdentifierResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBlocklistIdentifierBody,
) -> Response[
    Union[
        CreateBlocklistIdentifierResponse200,
        CreateBlocklistIdentifierResponse400,
        CreateBlocklistIdentifierResponse402,
        CreateBlocklistIdentifierResponse422,
    ]
]:
    """Add identifier to the block-list

     Create an identifier that is blocked from accessing an instance

    Args:
        body (CreateBlocklistIdentifierBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBlocklistIdentifierResponse200, CreateBlocklistIdentifierResponse400, CreateBlocklistIdentifierResponse402, CreateBlocklistIdentifierResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBlocklistIdentifierBody,
) -> Optional[
    Union[
        CreateBlocklistIdentifierResponse200,
        CreateBlocklistIdentifierResponse400,
        CreateBlocklistIdentifierResponse402,
        CreateBlocklistIdentifierResponse422,
    ]
]:
    """Add identifier to the block-list

     Create an identifier that is blocked from accessing an instance

    Args:
        body (CreateBlocklistIdentifierBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBlocklistIdentifierResponse200, CreateBlocklistIdentifierResponse400, CreateBlocklistIdentifierResponse402, CreateBlocklistIdentifierResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
