from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.set_user_profile_image_body import SetUserProfileImageBody
from ...models.set_user_profile_image_response_200 import SetUserProfileImageResponse200
from ...models.set_user_profile_image_response_400 import SetUserProfileImageResponse400
from ...models.set_user_profile_image_response_401 import SetUserProfileImageResponse401
from ...models.set_user_profile_image_response_404 import SetUserProfileImageResponse404
from ...types import Response


def _get_kwargs(
    user_id: str,
    *,
    body: SetUserProfileImageBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/users/{user_id}/profile_image",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        SetUserProfileImageResponse200,
        SetUserProfileImageResponse400,
        SetUserProfileImageResponse401,
        SetUserProfileImageResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SetUserProfileImageResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = SetUserProfileImageResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = SetUserProfileImageResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = SetUserProfileImageResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        SetUserProfileImageResponse200,
        SetUserProfileImageResponse400,
        SetUserProfileImageResponse401,
        SetUserProfileImageResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetUserProfileImageBody,
) -> Response[
    Union[
        SetUserProfileImageResponse200,
        SetUserProfileImageResponse400,
        SetUserProfileImageResponse401,
        SetUserProfileImageResponse404,
    ]
]:
    """Set user profile image

     Update a user's profile image

    Args:
        user_id (str):
        body (SetUserProfileImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[SetUserProfileImageResponse200, SetUserProfileImageResponse400, SetUserProfileImageResponse401, SetUserProfileImageResponse404]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetUserProfileImageBody,
) -> Optional[
    Union[
        SetUserProfileImageResponse200,
        SetUserProfileImageResponse400,
        SetUserProfileImageResponse401,
        SetUserProfileImageResponse404,
    ]
]:
    """Set user profile image

     Update a user's profile image

    Args:
        user_id (str):
        body (SetUserProfileImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[SetUserProfileImageResponse200, SetUserProfileImageResponse400, SetUserProfileImageResponse401, SetUserProfileImageResponse404]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetUserProfileImageBody,
) -> Response[
    Union[
        SetUserProfileImageResponse200,
        SetUserProfileImageResponse400,
        SetUserProfileImageResponse401,
        SetUserProfileImageResponse404,
    ]
]:
    """Set user profile image

     Update a user's profile image

    Args:
        user_id (str):
        body (SetUserProfileImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[SetUserProfileImageResponse200, SetUserProfileImageResponse400, SetUserProfileImageResponse401, SetUserProfileImageResponse404]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetUserProfileImageBody,
) -> Optional[
    Union[
        SetUserProfileImageResponse200,
        SetUserProfileImageResponse400,
        SetUserProfileImageResponse401,
        SetUserProfileImageResponse404,
    ]
]:
    """Set user profile image

     Update a user's profile image

    Args:
        user_id (str):
        body (SetUserProfileImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[SetUserProfileImageResponse200, SetUserProfileImageResponse400, SetUserProfileImageResponse401, SetUserProfileImageResponse404]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
