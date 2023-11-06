import pytest

from data_fixtures import USER, PASSWORD


@pytest.mark.usefixtures("db")
class TestAdmin:
    def test_create_user(self, db, test_app, admin_access_token):
        response = test_app.post(
            "/admin/users",
            json={
                "username": USER["username"],
                "password": PASSWORD,
                "email": USER["email"],
                "role": USER["role"],
            },
            headers={"Authorization": f"Bearer {admin_access_token}"},
        )
        assert response.status_code == 201

        # Check that the user was created
        assert (
            db.users.find_one({"username": USER["username"]})["username"]
            == USER["username"]
        )

    def test_create_user_username_conflict(self, db, test_app, admin_access_token):
        response = test_app.post(
            "/admin/users",
            json={
                "username": USER["username"],
                "password": PASSWORD,
                "email": USER["email"],
                "role": USER["role"],
            },
            headers={"Authorization": f"Bearer {admin_access_token}"},
        )
        assert response.status_code == 201

        response = test_app.post(
            "/admin/users",
            json={
                "username": USER["username"],
                "password": PASSWORD,
                "email": USER["email"],
                "role": USER["role"],
            },
            headers={"Authorization": f"Bearer {admin_access_token}"},
        )
        assert response.status_code == 400

    def test_create_user_non_admin(self, db, test_app, user_access_token):
        response = test_app.post(
            "/admin/users",
            json={
                "username": USER["username"],
                "password": PASSWORD,
                "email": USER["email"],
                "role": USER["role"],
            },
            headers={"Authorization": f"Bearer {user_access_token}"},
        )
        assert response.status_code == 401
