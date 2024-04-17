from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr

from app.users.dao import UsersDAO

from app.config import Config, load_config

config: Config = load_config()

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
        to_encode, config.auth_config.key, config.auth_config.algorithm
    )
    return encoded_jwt


async def authentificate_user(email: EmailStr, password: str):  # эта функция для аутентификации пользователя
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user
