"""
JWT Utilities. Use authorization in API initialization, and decorators on routes
"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, verify_jwt_in_request_optional
from src.utils.exceptions import SynbrowserException


def add_claims_to_jwt(identity):
    """

    :param identity:
    :return:
    """
    claims = {
        # Issuer (JWT Standard)
        'iss': 'jax.synbrowser.api',
        # Subject (JWT Standard)
        'sub': 'Identity',
        'aud': identity.get('email'),
        # User ID
        'uid': identity.get('id')
    }

    return claims


class UrlJwtMismatch(SynbrowserException):
    """
    Url and jwt don't agree about something
    """


def required_jwt_matches_url(url_param, claim_key):
    """

    :param url_param:
    :param claim_key:
    :return:
    """
    def meta_warp(fnc):
        @wraps(fnc)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if kwargs.get(url_param) != claims[claim_key]:
                raise UrlJwtMismatch('Route requires access token match url')
            return fnc(*args, **kwargs)
        return wrapper
    return meta_warp


def optional_jwt_matches_url(url_param, claim_key):
    """

    :param url_param:
    :param claim_key:
    :return:
    """
    def meta_warp(fnc):
        @wraps(fnc)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request_optional()
            claims = get_jwt_claims()
            if kwargs.get(url_param) != claims[claim_key]:
                raise UrlJwtMismatch('Route requires access token match url')
            return fnc(*args, **kwargs)
        return wrapper
    return meta_warp


def jwt_admin_required(fnc):
    """

    :param fnc:
    :return:
    """
    @wraps(fnc)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            raise UrlJwtMismatch('Route requires admin privileges')
        return fnc(*args, **kwargs)
    return wrapper
