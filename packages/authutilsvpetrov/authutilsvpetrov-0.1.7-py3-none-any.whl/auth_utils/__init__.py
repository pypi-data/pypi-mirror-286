"""
This module is used to provide the necessary classes and exceptions
for the authentication and authorization of users.
"""
from userutilsvpetrov.schemas import User
from userutilsvpetrov.schemas import Admin as AdminUser
from .exceptions import AuthorizationException
from .middlewares import require_admin_user, require_user

from .schemas import Token, TokenData, ValidationCode

__all__ = [
    "User",
    "AdminUser",
    "AuthorizationException",
    "require_admin_user",
    "require_user",
    "Token",
    "TokenData",
    "ValidationCode",
]
