import os


class Config:
    """Get configuration from environment variables."""

    def __init__(self):
        self.db_url = os.environ["MONGODB_URL"]
        self.db_name = os.environ["DB_NAME"]

        self.jwt_secret = os.environ["ACCESS_TOKEN_SECRET_KEY"]
        self.jwt_algorithm = os.environ["ACCESS_TOKEN_ALGORITHM"]
        self.jwt_expire = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])


config = Config()
