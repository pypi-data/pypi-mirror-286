from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_jwt_template_body import UpdateJWTTemplateBody
from ...models.update_jwt_template_response_200 import UpdateJWTTemplateResponse200
from ...models.update_jwt_template_response_400 import UpdateJWTTemplateResponse400
from ...models.update_jwt_template_response_402 import UpdateJWTTemplateResponse402
from ...models.update_jwt_template_response_422 import UpdateJWTTemplateResponse422
from ...types import Response


def _get_kwargs(
    template_id: str,
    *,
    body: UpdateJWTTemplateBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/jwt_templates/{template_id}",
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
        UpdateJWTTemplateResponse200,
        UpdateJWTTemplateResponse400,
        UpdateJWTTemplateResponse402,
        UpdateJWTTemplateResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateJWTTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateJWTTemplateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = UpdateJWTTemplateResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateJWTTemplateResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateJWTTemplateResponse200,
        UpdateJWTTemplateResponse400,
        UpdateJWTTemplateResponse402,
        UpdateJWTTemplateResponse422,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateJWTTemplateBody,
) -> Response[
    Union[
        UpdateJWTTemplateResponse200,
        UpdateJWTTemplateResponse400,
        UpdateJWTTemplateResponse402,
        UpdateJWTTemplateResponse422,
    ]
]:
    """Update a JWT template

     Updates an existing JWT template

    Args:
        template_id (str):
        body (UpdateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateJWTTemplateResponse200, UpdateJWTTemplateResponse400, UpdateJWTTemplateResponse402, UpdateJWTTemplateResponse422]]
    """

    kwargs = _get_kwargs(
        template_id=template_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateJWTTemplateBody,
) -> Optional[
    Union[
        UpdateJWTTemplateResponse200,
        UpdateJWTTemplateResponse400,
        UpdateJWTTemplateResponse402,
        UpdateJWTTemplateResponse422,
    ]
]:
    """Update a JWT template

     Updates an existing JWT template

    Args:
        template_id (str):
        body (UpdateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateJWTTemplateResponse200, UpdateJWTTemplateResponse400, UpdateJWTTemplateResponse402, UpdateJWTTemplateResponse422]
    """

    return sync_detailed(
        template_id=template_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateJWTTemplateBody,
) -> Response[
    Union[
        UpdateJWTTemplateResponse200,
        UpdateJWTTemplateResponse400,
        UpdateJWTTemplateResponse402,
        UpdateJWTTemplateResponse422,
    ]
]:
    """Update a JWT template

     Updates an existing JWT template

    Args:
        template_id (str):
        body (UpdateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateJWTTemplateResponse200, UpdateJWTTemplateResponse400, UpdateJWTTemplateResponse402, UpdateJWTTemplateResponse422]]
    """

    kwargs = _get_kwargs(
        template_id=template_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateJWTTemplateBody,
) -> Optional[
    Union[
        UpdateJWTTemplateResponse200,
        UpdateJWTTemplateResponse400,
        UpdateJWTTemplateResponse402,
        UpdateJWTTemplateResponse422,
    ]
]:
    """Update a JWT template

     Updates an existing JWT template

    Args:
        template_id (str):
        body (UpdateJWTTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateJWTTemplateResponse200, UpdateJWTTemplateResponse400, UpdateJWTTemplateResponse402, UpdateJWTTemplateResponse422]
    """

    return (
        await asyncio_detailed(
            template_id=template_id,
            client=client,
            body=body,
        )
    ).parsed
