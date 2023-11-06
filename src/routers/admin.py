from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database

from dependencies import get_db, get_admin_user
from models.users import create_user, UserAlreadyExists
from schemas.users import User, UserIn
from utils.auth import get_password_hash

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(get_admin_user)],
)


@router.post(
    "/users",
    response_description="Create a new user.",
    status_code=201,
    responses={400: {"description": "User already exists"}},
)
async def post_user(
    user: UserIn,
    db: Database = Depends(get_db),
) -> None:
    """Adds a new user to the database."""
    user = User(**user.model_dump(), hashed_password=get_password_hash(user.password))
    try:
        await create_user(db, user)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
