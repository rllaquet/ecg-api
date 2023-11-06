import copy

import pytest
from fastapi.testclient import TestClient
from pymongo.database import Database

from data_fixtures import USER, PASSWORD, ECG, DISABLED_USER


@pytest.mark.usefixtures("db")
class TestAuth:
    def test_access_ecg(self, db: Database, test_app: TestClient):
        # Insert a user and an ecg for said user
        db.users.insert_one(USER)
        db.ecg.insert_one(ECG)

        # Get access token
        response = test_app.post(
            "/auth/token", data={"username": USER["username"], "password": PASSWORD}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]

        # Try to access ecg with token
        response = test_app.get(
            f"/ecg/{ECG['_id']}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(ECG["_id"])

    def test_access_ecg_no_auth(self, db: Database, test_app: TestClient):
        response = test_app.get(
            f"/ecg/{ECG['_id']}",
        )
        assert response.status_code == 401

    def test_access_ecg_inactive_user(self, db: Database, test_app: TestClient):
        # Insert a user and an ecg for said user
        db.users.insert_one(DISABLED_USER)

        # Get access token
        response = test_app.post(
            "/auth/token",
            data={"username": DISABLED_USER["username"], "password": PASSWORD},
        )
        assert response.status_code == 401

    def test_access_ecg_inactive_user_after_acquiring_token(
        self, db: Database, test_app: TestClient
    ):
        # Insert a user and an ecg for said user
        db.users.insert_one(USER)

        # Get access token
        response = test_app.post(
            "/auth/token",
            data={"username": USER["username"], "password": PASSWORD},
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]

        # Disable user
        db.users.update_one(
            {"username": USER["username"]}, {"$set": {"disabled": True}}
        )

        # Try to access ecg with token
        response = test_app.get(
            f"/ecg/{ECG['_id']}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 401

    def test_access_ecg_wrong_user(self, db: Database, test_app: TestClient):
        # Insert a user and an ecg for said user
        db.users.insert_one(USER)

        # Insert an ECG for another user
        ecg = copy.deepcopy(ECG)
        ecg["user"] = DISABLED_USER["_id"]
        db.ecg.insert_one(ecg)

        # Get access token
        response = test_app.post(
            "/auth/token",
            data={"username": USER["username"], "password": PASSWORD},
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]

        # Try to access ecg with wrong user's token
        response = test_app.get(
            f"/ecg/{ECG['_id']}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 404
