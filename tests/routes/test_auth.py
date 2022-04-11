from random import randrange

from tests.routes.test_main import client

existing_user = {
    "username": "123",
    "email": "123",
    "full_name": "123",
    "password": "123",
}

# random str for user
x = str(randrange(0, 900000000000000000))
new_user = {"username": x, "email": x, "full_name": x, "password": x}


def test_unauthorised_access():
    response = client.get(url="/api/user/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_login():
    response = client.post(
        url="/api/auth/login",
        data={"grant_type": "password", "username": "123", "password": "123"},
    )
    assert response.status_code == 200
    assert len(response.json()["access_token"]) == 121
    assert response.json()["token_type"] == "bearer"
    pass


def test_invalid_registration():
    """Users email already registered"""
    response = client.post(url="/api/auth/register", json=existing_user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
    pass


def test_valid_registration():
    """User that doesnt exist"""
    response = client.post(url="/api/auth/register", json=new_user)
    assert response.status_code == 200
    assert response.json()["username"] == new_user["username"]
    assert response.json()["email"] == new_user["email"]
    assert response.json()["email"] == new_user["email"]
    assert response.json()["disabled"] is False
    pass
