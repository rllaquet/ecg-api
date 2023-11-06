from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database

from dependencies import get_db
from models.users import get_user
from schemas.auth import Token
from utils.auth import create_access_token, authenticate_user

router = APIRouter(
    prefix="/auth",
)


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Database = Depends(get_db),
):
    """Login endpoint. Returns access token."""
    user = await get_user(db, form_data.username)

    if not user or not authenticate_user(user, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
