from tests.routes.test_alert import random_user
from tests.routes.test_main import client

existing_user = {
    "username": "123",
    "email": "123",
    "full_name": "123",
    "password": "1234",
}

new_user = random_user()


def test_unauthorised_access():
    response = client.get(url="/api/user/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_login():
    response = client.post(
        url="/api/auth/login",
        data={
            "grant_type": "password",
            "username": existing_user["username"],
            "password": existing_user["password"],
        },
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
    assert response.json()["email"] == new_user["email"]
    assert response.json()["disabled"] is False
    pass


# group into a class?
def test_reset_password_flow():
    """Password Reset Flow:

    User forgets password, enters email address for reset link.
    Link is sent to email (with user_email and expiry in payload).
    User clicks link, if valid/not expired they're sent a Cookie w/ token.
    User redirected to password reset.
    """
    # forgot_password
    res1 = client.post(
        url="/api/auth/forgot_password_link",
        json={
            "email": new_user["email"],
        },
    )
    assert res1.status_code == 200
    assert res1.json()["message"] == "Reset Code sent to email"
    reset_link = res1.json()["reset_url"]

    # reset password
    res2 = client.get(reset_link)

    assert res2.json()["success"] == "Cookie created"
    cookies = res2.cookies.get_dict()
    print("ln 75:", cookies)

    # change_password
    res3 = client.post(
        url="/api/auth/change_password/",
        json={"password": "123"},
        cookies=cookies,
    )

    print("ln 85", res3.cookies.get_dict())
    print(res3.json())
    assert res3.status_code == 200
    assert res3.json()["success"] == "New Password"

    # test login
    res4 = client.post(
        url="/api/auth/login",
        data={
            "grant_type": "password",
            "username": new_user["username"],
            "password": "123",
        },
    )
    assert res4.status_code == 200
    assert res4.json()["token_type"] == "bearer"


def test_forgot_password_link():
    pass


def test_forgot_password_reset():
    pass


def test_change_password():
    pass


class test_reg_and_reset_flow:
    pass
