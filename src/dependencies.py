from typing import Annotated

import motor.motor_asyncio
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pymongo.database import Database

from config import config
from models.users import get_user
from schemas.auth import TokenData
from schemas.users import User


def get_db() -> Database:
    """Get database connection"""
    client = motor.motor_asyncio.AsyncIOMotorClient(config.db_url)
    db = client.get_database(config.db_name)
    try:
        yield db
    finally:
        client.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    db: Annotated[Database, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Get current user from token. If the token is invalid, raise an exception."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.jwt_secret, algorithms=[config.jwt_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None or user.disabled:
        raise credentials_exception
    return user


async def get_admin_user(
    db: Annotated[Database, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Extra check to ensure that the user is also an admin."""
    user = await get_current_user(db, token)
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not admin",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
