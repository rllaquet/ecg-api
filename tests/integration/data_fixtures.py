import pendulum
from bson import ObjectId

PASSWORD = "poteto"

ADMIN_USER = {
    "_id": ObjectId("654922244c1abb37ac03679b"),
    "username": "admin",
    "email": "admin@admin.io",
    "role": "admin",
    "hashed_password": "$2b$12$XkFCVbwBu8SNYu58v1WMnO3nDe9DRdxXO9AAd4dDxLdTZAU8SvVOG",
    "disabled": False,
}


USER = {
    "_id": ObjectId("654922244c1abb37ac03679a"),
    "username": "potato",
    "email": "potato@poteto.io",
    "role": "user",
    "hashed_password": "$2b$12$XkFCVbwBu8SNYu58v1WMnO3nDe9DRdxXO9AAd4dDxLdTZAU8SvVOG",
    "disabled": False,
}

DISABLED_USER = {
    "_id": ObjectId("654922244c1abb37ac03679d"),
    "username": "onion",
    "email": "onion@poteto.io",
    "role": "user",
    "hashed_password": "$2b$12$XkFCVbwBu8SNYu58v1WMnO3nDe9DRdxXO9AAd4dDxLdTZAU8SvVOG",
    "disabled": True,
}


ECG = {
    "_id": ObjectId("654922244c1abb37ac03679f"),
    "user": USER["_id"],
    "created_at": pendulum.from_timestamp(1699215153),
    "leads": [{"name": "I", "n_samples": 3, "signal": [3, 2, 1], "zero_crossings": 0}],
}
