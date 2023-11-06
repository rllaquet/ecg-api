"""Database model for ECGs."""
from pymongo.database import Database

from schemas.users import User, UserOut


class UserAlreadyExists(Exception):
    pass


async def get_user(db: Database, username: str) -> UserOut | None:
    """Get a single user from the DB by username.

    Args:
        db: instance of MongoDB database.
        username: username of the user to be fetched.

    Returns:
        UserOut: User object.
    """
    user = await db.users.find_one({"username": username})
    if user:
        return UserOut(**user, id=str(user["_id"]))
    return None


async def create_user(db, user: User) -> str | None:
    """Add a new user to the database.

    Args:
        db: instance of MongoDB database.
        user: User to be added to the database.

    Returns:
        str: inserted user id.
    """
    if await get_user(db, user.username):
        raise UserAlreadyExists
    result = await db.users.insert_one(user.model_dump())
    return result.inserted_id
