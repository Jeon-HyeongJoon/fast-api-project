from fastapi import HTTPException
from starlette import status


class CommonExceptions:
    OBJECT_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="object not found",
    )


class AuthExceptions:
    INCORRECT_FORM = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    INVALID_FULLNAME_LENGTH = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Invalid fullname length. (0 < length < 128)",
    )
    SESSION_NOT_FOUND = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not found"
    )
    SESSION_UNKNOWN = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Session logged out"
    )

    INVALID_PASSWORD_LENGTH = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Invalid password length. (8 < length)",
    )
    EMAIL_EXISTS = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Email already exists",
    )
    USER_NAME_EXISTS = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="User name already exists",
    )
