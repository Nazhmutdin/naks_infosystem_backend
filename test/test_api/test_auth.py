from httpx import Cookies
import pytest

from client import client


@pytest.mark.usefixtures("add_users")
@pytest.mark.usefixtures("prepare_db")
class TestAuthEndpoints:

    def test_authenticate(self):
        res = client.post(
            "/auth/authenticate",
            json={
                "login": "TestUser",
                "password": "QWE123df"
            }
        )

        assert res.status_code == 200

        client.cookies = Cookies({"access_token": res.cookies.get("access_token")})