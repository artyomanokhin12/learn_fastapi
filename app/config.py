from dataclasses import dataclass
from environs import Env


@dataclass
class HostConfig:

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str


@dataclass
class AuthConfig:

    key: str
    algorithm: str


@dataclass
class SMTP:
    host: str 
    port: str 
    user: str 
    password: str 


@dataclass
class Config:

    host_config: HostConfig
    auth_config: AuthConfig
    smtp_service: SMTP


def load_config(path: str | None = None) -> Config:

    env = Env()
    env.read_env()

    return Config(
        host_config = HostConfig(
            DB_NAME=env("DB_NAME"),
            DB_PASS=env("DB_PASS"),
            DB_PORT=env("DB_PORT"),
            DB_USER=env("DB_USER"),
            DB_HOST=env("DB_HOST")
        ),
        auth_config=AuthConfig(
            key=env("auth_key"),
            algorithm=env("auth_algorythm")
        ),
        smtp_service=SMTP(
            host=env("SMTP_HOST"),
            port=env("SMTP_PORT"),
            user=env("SMTP_USER"),
            password=env("SMTP_PASS")
        )
    )
