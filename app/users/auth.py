from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:  # функция создана для создания токена
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_KEY, settings.AUTH_ALGORITHM
    )
    return encoded_jwt


async def authentificate_user(email: EmailStr, password: str):  # эта функция для аутентификации пользователя
    user = await UsersDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user
