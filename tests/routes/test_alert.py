from random import randrange

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# test the new alert route

# user entered invalid asin
# user already has alert for item
# user has 5+ alerts

# item is deactive
# item doesnt exist, create it


existing_user = {
    "username": "123",
    "email": "123",
    "full_name": "123",
    "password": "123",
}

existing_item = "https://www.amazon.co.uk/dp/B07PPTN43Y"
invalid_url = "https://www.amazon.co.u7PPTN43Y"


# random str for user
def random_user():
    x = str(randrange(0, 900000000000000000))
    return {"username": x, "email": x, "full_name": x, "password": x}


def test_invalid_asin():
    pass


def test_fiveplus_alerts():
    pass


def test_deactivated_item():
    pass
