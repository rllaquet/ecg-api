import argparse
import os

from bson import ObjectId
from passlib.context import CryptContext
from pymongo import MongoClient

ADMIN_USER = {
    "_id": ObjectId(),
    "username": "admin",
    "email": "admin@admin.io",
    "role": "admin",
    "disabled": False,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an admin user on MongoDB")
    parser.add_argument("-u", "--user", default="admin")
    parser.add_argument("-p", "--password", default="admin")
    args = parser.parse_args()

    # Set username
    ADMIN_USER["username"] = args.user

    # Hash password
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ADMIN_USER["hashed_password"] = pwd_context.hash(args.password)

    client = MongoClient(
        os.environ["MONGODB_URL"], os.environ.get("ECG_MONGO_PORT", 27017)
    )
    db = client.get_database(os.environ["DB_NAME"])
    db.users.insert_one(ADMIN_USER)
    print(f"Created admin user with credentials {args.user}:{args.password}")
