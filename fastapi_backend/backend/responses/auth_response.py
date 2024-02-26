import logging

from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

__all__ = (
    "login_responses",
    "sign_up_responses",
)

logger = logging.getLogger("dev")

sign_up_responses = {
    HTTP_409_CONFLICT: {
        "description": "The transmitted email address is not unique within "
        "the database.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "This email is already in use by another "
                    "user.",
                },
            },
        },
    },
    HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Any database error when saving the user.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Any error related to saving the user to "
                    "the database.",
                },
            },
        },
    },
}

login_responses = {
    HTTP_403_FORBIDDEN: {
        "description": "The password for the found user does not match.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Passwords did not match.",
                },
            },
        },
    },
    HTTP_404_NOT_FOUND: {
        "description": "The user was not found based on the login provided.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "A user with this login was not found.",
                },
            },
        },
    },
    HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Any database error when searching the user.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "string",
                },
            },
        },
    },
}
