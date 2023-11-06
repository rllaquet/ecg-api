from enum import Enum

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role


class UserIn(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "username",
                    "email": "email@email.com",
                    "password": "password",
                    "role": "user",
                }
            ]
        }
    }


class User(UserBase):
    hashed_password: str
    disabled: bool = False


class UserOut(User):
    id: str
