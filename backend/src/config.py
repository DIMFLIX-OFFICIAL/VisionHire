from pathlib import Path

from environs import Env

env = Env()
env.read_env()

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
PROJECT_SRC = PROJECT_ROOT / "src"
USERS_AVATARS = PROJECT_SRC / "avatars" / "users"
DEFAULT_DIRECTOR_AVATAR = PROJECT_SRC / "avatars" / "director-avatar.png"
DEFAULT_RECRUITER_AVATAR = PROJECT_SRC / "avatars" / "recruiter-avatar.png"

JWT_TOKEN_SECRET = env.str("JWT_TOKEN_SECRET")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = env.int("JWT_ACCESS_TOKEN_EXPIRES")
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = env.int("JWT_REFRESH_TOKEN_EXPIRES")
JWT_ALGORITHM = env.str("JWT_ALGORITHM", default="HS256")

API_HOST = env.str("API_HOST")
API_PORT = env.int("API_PORT")

DB_HOST = env.str("DB_HOST")
DB_PORT = env.int("DB_PORT")
DB_USERNAME = env.str("DB_USERNAME")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_NAME = env.str("DB_NAME")
DB_URL: str = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SMTP_HOST = env.str("SMTP_HOST")
SMTP_PORT = env.int("SMTP_PORT")
EMAIL = env.str("EMAIL")
EMAIL_PASSWORD = env.str("EMAIL_PASSWORD")

ADMIN_LOGIN = env.str("ADMIN_LOGIN")
ADMIN_PASSWORD = env.str("ADMIN_PASSWORD")