import pytest
from httpx import AsyncClient

@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kot1@pes.com", "1234", 200),
        ("kot2@pes.com", "12345", 200),
        ("kot1@pes.com", "123456", 409),
        ("abcde", "123456", 422),
        ("adsad@2adasdA", "123456", 422),
    ],
)
async def test_auth_flow(email: str, password: str, status_code: int, ac: AsyncClient):
    # /register
    resp_register = await ac.post("/auth/register", json={"email": email, "password": password})
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post("/auth/login", json={"email": email, "password": password})
    assert ac.cookies["access_token"]
    assert resp_register.status_code == status_code
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await ac.get("/auth/me")
    assert resp_register.status_code == status_code
    user = resp_me.json()
    assert "id" in user
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    resp_logout = await ac.post("/auth/logout")
    assert resp_register.status_code == status_code
    assert "access_token " not in resp_logout.cookies
