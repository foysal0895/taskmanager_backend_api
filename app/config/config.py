import os
from dotenv import load_dotenv
import datetime
import jwt
import bcrypt

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/postgres",
)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def encode_access_token(user_id:int,email:str):
    exp=datetime.datetime.now()+datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"user_id":user_id,"email":email,"exp":exp}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_access_token(token:str):
    decoded=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    return decoded


def hash_password(password:str):
    salt=bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"),salt).decode("utf-8")


def verify_password(password:str,hashed_password:str):
    return bcrypt.checkpw(password.encode("utf-8"),hashed_password.encode("utf-8"))