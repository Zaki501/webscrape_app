from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "7deaa6f0fdd89d91b8b824f35708dcd73db19b6b0921fc85fdc2be9ff1f8b067"
ENCODED_SECRET = "G5SGKYLBGZTDAZTEMQ4DSZBZGFRDQYRYGI2GMMZVG4YDQZDDMQ3TGZDCGE4WENTCGA4TEMLGMM4DKZTEMMZGEZJZMZTDCZRYMIYDMNY='"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_hash(password):
    return pwd_context.hash(password)


def verify_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
