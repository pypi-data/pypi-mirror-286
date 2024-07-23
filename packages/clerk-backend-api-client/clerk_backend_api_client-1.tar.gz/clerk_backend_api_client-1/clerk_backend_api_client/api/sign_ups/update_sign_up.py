from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_sign_up_body import UpdateSignUpBody
from ...models.update_sign_up_response_200 import UpdateSignUpResponse200
from ...models.update_sign_up_response_403 import UpdateSignUpResponse403
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: UpdateSignUpBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/sign_ups/{id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateSignUpResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UpdateSignUpResponse403.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSignUpBody,
) -> Response[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]:
    """Update a sign-up

     Update the sign-up with the given ID

    Args:
        id (str):
        body (UpdateSignUpBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSignUpBody,
) -> Optional[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]:
    """Update a sign-up

     Update the sign-up with the given ID

    Args:
        id (str):
        body (UpdateSignUpBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateSignUpResponse200, UpdateSignUpResponse403]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSignUpBody,
) -> Response[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]:
    """Update a sign-up

     Update the sign-up with the given ID

    Args:
        id (str):
        body (UpdateSignUpBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSignUpBody,
) -> Optional[Union[UpdateSignUpResponse200, UpdateSignUpResponse403]]:
    """Update a sign-up

     Update the sign-up with the given ID

    Args:
        id (str):
        body (UpdateSignUpBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateSignUpResponse200, UpdateSignUpResponse403]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
