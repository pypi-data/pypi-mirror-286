# -*- coding: utf-8 -*-
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import aiohttp
import jose.exceptions
from mantis_authz.config import authz_config
from mantis_authz.models import Token
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OpenIdConnect as FastAPIOpenIdConnect
from fastapi.security import SecurityScopes
from fastapi.security.base import SecurityBase
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBase
from jose import jwt
from keycloak import KeycloakOpenID
from keycloak import KeycloakOpenIDConnection
from keycloak import KeycloakUMA
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from typing_extensions import Annotated


class OpenIdConnect(FastAPIOpenIdConnect):
    """
    Class inheriting from `fastapi.security.OpenIdConnect`, that fixes the
    status code when the authorization header is absent (403 => 401).
    """

    async def __call__(self, request: Request) -> Response:
        try:
            return await super().__call__(request)
        except HTTPException as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=e.detail
            )  # noqa: F811


class MantisOpenID(KeycloakOpenID):
    """
    Pre-configured Keycloak OIDC.
    """

    def __init__(self) -> None:
        super().__init__(
            server_url=authz_config.server_url,
            realm_name=authz_config.realm,
            client_id=authz_config.client_id,
            client_secret_key=authz_config.client_secret,
            verify=authz_config.verify_ssl,
        )


class MantisUMA(KeycloakUMA):
    """
    Pre-configured Keycloak UMA client.
    """

    def __init__(self, token: Optional[Dict] = None) -> None:
        super().__init__(
            connection=KeycloakOpenIDConnection(
                server_url=authz_config.server_url,
                realm_name=authz_config.realm,
                client_id=authz_config.client_id,
                client_secret_key=authz_config.client_secret,
                verify=authz_config.verify_ssl,
                token=token,
            )
        )


def get_oidc_scheme() -> SecurityBase:
    if authz_config.use_permissions:
        oidc_scheme = OpenIdConnect(openIdConnectUrl=authz_config.discovery_url)
    else:
        # dummy authenticator use to respect endpoint definitions
        oidc_scheme = HTTPBase(scheme="null", auto_error=False)
    return oidc_scheme


async def get_jwk(kid: str) -> Optional[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            authz_config.discovery_url, ssl=authz_config.verify_ssl
        ) as response:
            data = await response.json()
        jwks_uri = data["jwks_uri"]
        async with session.get(jwks_uri, ssl=authz_config.verify_ssl) as response:
            data = await response.json()
    jwks = data["keys"]
    return next((jwk for jwk in jwks if kid == jwk["kid"]), None)


async def get_jwt_token_fastapi(
    security_scopes: SecurityScopes,
    token_header: Annotated[
        Union[HTTPAuthorizationCredentials, str, None], Depends(get_oidc_scheme())
    ],
) -> Optional[Token]:
    return await get_jwt_token(security_scopes.scopes, token_header)


async def get_jwt_token(
    scopes: List[str],
    token_header: Annotated[
        Union[HTTPAuthorizationCredentials, str, None], Depends(get_oidc_scheme())
    ],
) -> Optional[Token]:
    # Handle missing token header
    if token_header is None:
        if authz_config.use_permissions:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer token required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return None

    # Handle str formatted token header
    if isinstance(token_header, str):
        token_header_type, token_raw_data = token_header.split(maxsplit=1)
        token_header = HTTPAuthorizationCredentials(
            scheme=token_header_type, credentials=token_raw_data
        )

    assert isinstance(token_header, HTTPAuthorizationCredentials)
    expected_token_types = ("Bearer",)
    if token_header.scheme not in expected_token_types:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": expected_token_types[0]},
        )
    token_headers = jwt.get_unverified_header(token_header.credentials)
    token_type = token_headers["typ"]
    if token_type != "JWT":
        raise ValueError("Invalid token type %r" % token_type)

    token_data: dict
    if authz_config.use_permissions:
        token_jwk = await get_jwk(token_headers["kid"])
        if token_jwk is None or token_headers["alg"] != token_jwk["alg"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid",
                headers={"WWW-Authenticate": expected_token_types[0]},
            )
        try:
            token_data = jwt.decode(
                token_header.credentials,
                token_jwk,
                audience=authz_config.client_id,
            )
        except jose.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": expected_token_types[0]},
            )
        for scope in scopes:
            if scope not in token_data["scope"].split():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permission",
                    headers={"WWW-Authenticate": expected_token_types[0]},
                )
    else:
        token_data = jwt.get_unverified_claims(token_header.credentials)
    return Token(
        raw=token_header.credentials,
        decoded=token_data,
        header_auth_type=token_header.scheme,
    )
