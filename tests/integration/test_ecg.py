import pytest
from bson import ObjectId

from data_fixtures import ECG


@pytest.mark.usefixtures("db")
class TestECG:
    def test_post_ecg(self, test_app, user_access_token):
        ecg_data = {"leads": [{"name": "I", "n_samples": 3, "signal": [12, 2, 3]}]}
        response = test_app.post(
            "/ecg/",
            json=ecg_data,
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 201

    def test_post_ecg_wrong_data(self, test_app, user_access_token):
        ecg_data = {"leads": [{"name": "I", "signal": "[1, 2, 3]"}]}
        response = test_app.post(
            "/ecg/",
            json=ecg_data,
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 422

    def test_post_ecg_missing_data(self, test_app, user_access_token):
        ecg_data = {"leads": [{"name": "I"}]}
        response = test_app.post(
            "/ecg/",
            json=ecg_data,
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 422

    def test_get_ecg(self, db, test_app, user_access_token):
        db.ecg.insert_one(ECG)
        ecg_id = str(ECG["_id"])

        response = test_app.get(
            f"/ecg/{ecg_id}", headers={"Authorization": f"Bearer {user_access_token}"}
        )
        assert response.status_code == 200
        assert response.json()["id"] == ecg_id

    def test_get_ecg_invalid_id(self, test_app, user_access_token):
        ecg_id = "invalid_ecg_id"
        response = test_app.get(
            f"/ecg/{ecg_id}", headers={"Authorization": f"Bearer {user_access_token}"}
        )
        assert response.status_code == 400

    def test_get_ecg_not_found(self, test_app, user_access_token):
        ecg_id = ObjectId()
        response = test_app.get(
            f"/ecg/{ecg_id}", headers={"Authorization": f"Bearer {user_access_token}"}
        )
        assert response.status_code == 404
