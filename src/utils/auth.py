import pendulum
from jose import jwt
from passlib.context import CryptContext

from config import config
from schemas.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a password and a hashed_password match."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get the hash of a password."""
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: pendulum.Duration | None = None,
) -> str:
    """Create a JWT token with the given data.

    Args:
        data: Data to be encoded in the JWT token.
        expires_delta: Time delta for the token to expire.

    Returns:
        The encoded JWT token.
    """
    if not expires_delta:
        expires_delta = pendulum.duration(minutes=config.jwt_expire)
    to_encode = data.copy()
    expire = pendulum.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.jwt_secret, algorithm=config.jwt_algorithm
    )
    return encoded_jwt


def authenticate_user(user: User, password: str) -> bool:
    """Check if the password is valid for the given user."""
    if user.disabled:
        return False
    return verify_password(password, user.hashed_password)
