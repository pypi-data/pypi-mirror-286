from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_production_instance_domain_body import UpdateProductionInstanceDomainBody
from ...models.update_production_instance_domain_response_400 import UpdateProductionInstanceDomainResponse400
from ...models.update_production_instance_domain_response_422 import UpdateProductionInstanceDomainResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: UpdateProductionInstanceDomainBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": "/beta_features/domain",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = cast(Any, None)
        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateProductionInstanceDomainResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateProductionInstanceDomainResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateProductionInstanceDomainBody,
) -> Response[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]:
    """Update production instance domain

     Change the domain of a production instance.

    Changing the domain requires updating the [DNS
    records](https://clerk.com/docs/deployments/overview#dns-records) accordingly, deploying new [SSL
    certificates](https://clerk.com/docs/deployments/overview#deploy), updating your Social Connection's
    redirect URLs and setting the new keys in your code.

    WARNING: Changing your domain will invalidate all current user sessions (i.e. users will be logged
    out). Also, while your application is being deployed, a small downtime is expected to occur.

    Args:
        body (UpdateProductionInstanceDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]
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
    body: UpdateProductionInstanceDomainBody,
) -> Optional[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]:
    """Update production instance domain

     Change the domain of a production instance.

    Changing the domain requires updating the [DNS
    records](https://clerk.com/docs/deployments/overview#dns-records) accordingly, deploying new [SSL
    certificates](https://clerk.com/docs/deployments/overview#deploy), updating your Social Connection's
    redirect URLs and setting the new keys in your code.

    WARNING: Changing your domain will invalidate all current user sessions (i.e. users will be logged
    out). Also, while your application is being deployed, a small downtime is expected to occur.

    Args:
        body (UpdateProductionInstanceDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateProductionInstanceDomainBody,
) -> Response[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]:
    """Update production instance domain

     Change the domain of a production instance.

    Changing the domain requires updating the [DNS
    records](https://clerk.com/docs/deployments/overview#dns-records) accordingly, deploying new [SSL
    certificates](https://clerk.com/docs/deployments/overview#deploy), updating your Social Connection's
    redirect URLs and setting the new keys in your code.

    WARNING: Changing your domain will invalidate all current user sessions (i.e. users will be logged
    out). Also, while your application is being deployed, a small downtime is expected to occur.

    Args:
        body (UpdateProductionInstanceDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateProductionInstanceDomainBody,
) -> Optional[Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]]:
    """Update production instance domain

     Change the domain of a production instance.

    Changing the domain requires updating the [DNS
    records](https://clerk.com/docs/deployments/overview#dns-records) accordingly, deploying new [SSL
    certificates](https://clerk.com/docs/deployments/overview#deploy), updating your Social Connection's
    redirect URLs and setting the new keys in your code.

    WARNING: Changing your domain will invalidate all current user sessions (i.e. users will be logged
    out). Also, while your application is being deployed, a small downtime is expected to occur.

    Args:
        body (UpdateProductionInstanceDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, UpdateProductionInstanceDomainResponse400, UpdateProductionInstanceDomainResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
