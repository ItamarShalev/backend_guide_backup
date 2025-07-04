import logging
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.utils import Utils


class AuthUtility:

    _environment = Utils.environment()
    logging.getLogger('passlib').setLevel(logging.ERROR)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    SUPER_SECRET_KEY = _environment.SUPER_SECRET_KEY
    ALGORITHM = _environment.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = _environment.ACCESS_TOKEN_EXPIRE_MINUTES


    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return AuthUtility.pwd_context.verify(plain, hashed)


    @staticmethod
    def hash_password(password: str) -> str:
        return AuthUtility.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expires_delta = expires_delta or timedelta(minutes=AuthUtility.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            AuthUtility.SUPER_SECRET_KEY,
            algorithm=AuthUtility.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> str | None:
        try:
            payload = jwt.decode(
                token,
                AuthUtility.SUPER_SECRET_KEY,
                algorithms=[AuthUtility.ALGORITHM]
            )
            return payload.get("sub")
        except JWTError:
            return None
