from datetime import UTC, datetime, timedelta

from jose import jwt

from src.auth_utility import AuthUtility


def test_hash_and_verify_password():
    password = "mysecret"
    hashed = AuthUtility.hash_password(password)
    assert hashed != password
    assert AuthUtility.verify_password(password, hashed)
    assert not AuthUtility.verify_password("wrongpassword", hashed)

def test_create_access_token_contains_exp_and_data():
    data = {"sub": "user1"}
    token = AuthUtility.create_access_token(data)
    decoded = jwt.decode(token, AuthUtility.SUPER_SECRET_KEY, algorithms=[AuthUtility.ALGORITHM])
    assert "exp" in decoded
    assert decoded["sub"] == "user1"

def test_create_access_token_custom_expiry():
    data = {"sub": "user2"}
    expires = timedelta(minutes=5)
    token = AuthUtility.create_access_token(data, expires_delta=expires)
    decoded = jwt.decode(token, AuthUtility.SUPER_SECRET_KEY, algorithms=[AuthUtility.ALGORITHM])
    exp = datetime.fromtimestamp(decoded["exp"], UTC)
    now = datetime.now(UTC)
    assert timedelta(minutes=4) <= (exp - now) <= timedelta(minutes=6)

def test_decode_access_token_valid():
    data = {"sub": "user3"}
    token = AuthUtility.create_access_token(data)
    sub = AuthUtility.decode_access_token(token)
    assert sub == "user3"

def test_decode_access_token_invalid():
    invalid_token = "invalid.token.value"
    assert AuthUtility.decode_access_token(invalid_token) is None

def test_decode_access_token_expired():
    data = {"sub": "user4"}
    token = AuthUtility.create_access_token(data, expires_delta=timedelta(seconds=-1))
    assert AuthUtility.decode_access_token(token) is None
