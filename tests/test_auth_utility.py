from datetime import UTC, datetime, timedelta

from jose import jwt

from src import auth_utility


def test_hash_and_verify_password():
    password = "mysecret"
    hashed = auth_utility.hash_password(password)
    assert hashed != password
    assert auth_utility.verify_password(password, hashed)
    assert not auth_utility.verify_password("wrongpassword", hashed)

def test_create_access_token_contains_exp_and_data():
    data = {"sub": "user1"}
    token = auth_utility.create_access_token(data)
    decoded = jwt.decode(token, auth_utility.SECRET_KEY, algorithms=[auth_utility.ALGORITHM])
    assert "exp" in decoded
    assert decoded["sub"] == "user1"

def test_create_access_token_custom_expiry():
    data = {"sub": "user2"}
    expires = timedelta(minutes=5)
    token = auth_utility.create_access_token(data, expires_delta=expires)
    decoded = jwt.decode(token, auth_utility.SECRET_KEY, algorithms=[auth_utility.ALGORITHM])
    exp = datetime.fromtimestamp(decoded["exp"], UTC)
    now = datetime.now(UTC)
    assert timedelta(minutes=4) <= (exp - now) <= timedelta(minutes=6)

def test_decode_access_token_valid():
    data = {"sub": "user3"}
    token = auth_utility.create_access_token(data)
    sub = auth_utility.decode_access_token(token)
    assert sub == "user3"

def test_decode_access_token_invalid():
    invalid_token = "invalid.token.value"
    assert auth_utility.decode_access_token(invalid_token) is None

def test_decode_access_token_expired():
    data = {"sub": "user4"}
    token = auth_utility.create_access_token(data, expires_delta=timedelta(seconds=-1))
    assert auth_utility.decode_access_token(token) is None
