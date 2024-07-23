from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.upsert_template_body import UpsertTemplateBody
from ...models.upsert_template_response_200 import UpsertTemplateResponse200
from ...models.upsert_template_response_400 import UpsertTemplateResponse400
from ...models.upsert_template_response_401 import UpsertTemplateResponse401
from ...models.upsert_template_response_402 import UpsertTemplateResponse402
from ...models.upsert_template_response_403 import UpsertTemplateResponse403
from ...models.upsert_template_response_404 import UpsertTemplateResponse404
from ...models.upsert_template_response_422 import UpsertTemplateResponse422
from ...models.upsert_template_template_type import UpsertTemplateTemplateType
from ...types import Response


def _get_kwargs(
    template_type: UpsertTemplateTemplateType,
    slug: str,
    *,
    body: UpsertTemplateBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/templates/{template_type}/{slug}",
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
        UpsertTemplateResponse200,
        UpsertTemplateResponse400,
        UpsertTemplateResponse401,
        UpsertTemplateResponse402,
        UpsertTemplateResponse403,
        UpsertTemplateResponse404,
        UpsertTemplateResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpsertTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpsertTemplateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = UpsertTemplateResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = UpsertTemplateResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UpsertTemplateResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpsertTemplateResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpsertTemplateResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpsertTemplateResponse200,
        UpsertTemplateResponse400,
        UpsertTemplateResponse401,
        UpsertTemplateResponse402,
        UpsertTemplateResponse403,
        UpsertTemplateResponse404,
        UpsertTemplateResponse422,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_type: UpsertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertTemplateBody,
) -> Response[
    Union[
        UpsertTemplateResponse200,
        UpsertTemplateResponse400,
        UpsertTemplateResponse401,
        UpsertTemplateResponse402,
        UpsertTemplateResponse403,
        UpsertTemplateResponse404,
        UpsertTemplateResponse422,
    ]
]:
    """Update a template for a given type and slug

     Updates the existing template of the given type and slug

    Args:
        template_type (UpsertTemplateTemplateType):
        slug (str):
        body (UpsertTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpsertTemplateResponse200, UpsertTemplateResponse400, UpsertTemplateResponse401, UpsertTemplateResponse402, UpsertTemplateResponse403, UpsertTemplateResponse404, UpsertTemplateResponse422]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        slug=slug,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_type: UpsertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertTemplateBody,
) -> Optional[
    Union[
        UpsertTemplateResponse200,
        UpsertTemplateResponse400,
        UpsertTemplateResponse401,
        UpsertTemplateResponse402,
        UpsertTemplateResponse403,
        UpsertTemplateResponse404,
        UpsertTemplateResponse422,
    ]
]:
    """Update a template for a given type and slug

     Updates the existing template of the given type and slug

    Args:
        template_type (UpsertTemplateTemplateType):
        slug (str):
        body (UpsertTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpsertTemplateResponse200, UpsertTemplateResponse400, UpsertTemplateResponse401, UpsertTemplateResponse402, UpsertTemplateResponse403, UpsertTemplateResponse404, UpsertTemplateResponse422]
    """

    return sync_detailed(
        template_type=template_type,
        slug=slug,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    template_type: UpsertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertTemplateBody,
) -> Response[
    Union[
        UpsertTemplateResponse200,
        UpsertTemplateResponse400,
        UpsertTemplateResponse401,
        UpsertTemplateResponse402,
        UpsertTemplateResponse403,
        UpsertTemplateResponse404,
        UpsertTemplateResponse422,
    ]
]:
    """Update a template for a given type and slug

     Updates the existing template of the given type and slug

    Args:
        template_type (UpsertTemplateTemplateType):
        slug (str):
        body (UpsertTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpsertTemplateResponse200, UpsertTemplateResponse400, UpsertTemplateResponse401, UpsertTemplateResponse402, UpsertTemplateResponse403, UpsertTemplateResponse404, UpsertTemplateResponse422]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        slug=slug,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_type: UpsertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertTemplateBody,
) -> Optional[
    Union[
        UpsertTemplateResponse200,
        UpsertTemplateResponse400,
        UpsertTemplateResponse401,
        UpsertTemplateResponse402,
        UpsertTemplateResponse403,
        UpsertTemplateResponse404,
        UpsertTemplateResponse422,
    ]
]:
    """Update a template for a given type and slug

     Updates the existing template of the given type and slug

    Args:
        template_type (UpsertTemplateTemplateType):
        slug (str):
        body (UpsertTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpsertTemplateResponse200, UpsertTemplateResponse400, UpsertTemplateResponse401, UpsertTemplateResponse402, UpsertTemplateResponse403, UpsertTemplateResponse404, UpsertTemplateResponse422]
    """

    return (
        await asyncio_detailed(
            template_type=template_type,
            slug=slug,
            client=client,
            body=body,
        )
    ).parsed
