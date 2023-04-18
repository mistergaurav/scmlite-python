import datetime as dt
from typing import Dict, Optional
from typing import List

from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi import  Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext

from config.config import SETTING
from models.models import User

load_dotenv()
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SIGNUP_COLLECTION = SETTING.SIGNUP_COLLECTION
def hash_password(password: str):
    return PWD_CONTEXT.hash(password)


def verify_password(password: str, hashed_password: str):
    return PWD_CONTEXT.verify(password, hashed_password)


def get_user(email: str) -> User:
    user = SIGNUP_COLLECTION.find_one({"Email":email})
    if user:
        return user
    return None



class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str, scheme_name: Optional[str] = None, scopes: Optional[Dict[str, str]] = None, description: Optional[str] = None, auto_error: bool = True):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(SETTING.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                #redirect to login page
            return None
        return param

OAUTH2_SCHEME = OAuth2PasswordBearerWithCookie(tokenUrl="token")

def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=SETTING.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SETTING.SECRET_KEY,
        algorithm=SETTING.ALGORITHM
    )
    return encoded_jwt

def authenticate_user(username: str, plain_password: str) -> User:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(plain_password, user['Password']):
        return False
    return user

def decode_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials."
    )
    token = str(token).replace("Bearer", "").strip()

    try:
        payload = jwt.decode(token, SETTING.SECRET_KEY, algorithms=[SETTING.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = get_user(username)
    return user

def get_current_user_from_token(token: str = Depends(OAUTH2_SCHEME)) -> User:
    user = decode_token(token)
    return user

def get_current_user_from_cookie(request: Request) -> User:
    token = request.cookies.get(SETTING.COOKIE_NAME)
    user = decode_token(token)
    return user




class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors = []
        self.login_user = None
        self.login_password = None

    async def load_data(self):
        form = await self.request.form()
        self.login_user = form.get("login_user")
        self.login_password = form.get("login_password")

    async def is_valid(self):
        if not self.login_user or "@" not in self.login_user:
            self.errors.append("Email is required")
        if not self.login_password or len(self.login_password) < 4:
            self.errors.append("A valid password is required")
        return not self.errors
