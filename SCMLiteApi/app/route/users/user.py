
import random
import string
import datetime as dt
from typing import Dict, List, Optional
from dotenv import load_dotenv
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import JWTError, jwt
from config.config import SETTING
from models.models import User
from route.users.user_authentication import *


load_dotenv()

APP = APIRouter()

APP.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

CLIENT = SETTING.CLIENT
@APP.post("token")
def login_for_access_token(response: Response,\
    form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    # Authenticate the user with the provided credentials
    user = authenticate_user(form_data.login_user, form_data.login_password)
    if not user:
        # If the user is not authenticated, raise an HTTPException with 401 status code
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, \
            detail="Incorrect username or password")

    # Create an access token for the authenticated user
    access_token = create_access_token(data={"username": user["Email"]})

    # Set an HttpOnly cookie in the response.
    response.set_cookie(
        key=SETTING.COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True
    )
    # Return the access token and token type in a dictionary
    return {SETTING.COOKIE_NAME: access_token, "token_type": "bearer"}

LOGIN_TEMPLATE = "login.html"

# ----------------------------------------------------------------------
# Home 
# ----------------------------------------------------------------------
@APP.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    user = None
    try:
        user = get_current_user_from_cookie(request)
    except ValueError:
        pass
    return TEMPLATES.TemplateResponse("home.html", {"user": user, "request": request})

####################
# Login - GET
####################

@APP.get("/auth/login", response_class=HTMLResponse)
def login_get(request: Request, message: str = None):
    return TEMPLATES.TemplateResponse(LOGIN_TEMPLATE, {"request": request, "message": message})

####################
# Login - POST
####################

@APP.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request):
    form = LoginForm(request)
    await form.load_data()
    try:
        if not await form.is_valid():
            raise HTTPException(status_code=400, detail="Form data is not valid")
        response = RedirectResponse("/", status.HTTP_302_FOUND)
        login_for_access_token(response=response, form_data=form)
        form.__dict__.update(msg="Login Successful!")
        return response
    except HTTPException as e:
        form.__dict__.update(msg="", errors=[e.detail])
        return TEMPLATES.TemplateResponse(LOGIN_TEMPLATE, form.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

####################
# signup - GET
####################
@APP.get("/signup", response_class=HTMLResponse)
def signup_get(request: Request):
    try:
        return TEMPLATES.TemplateResponse("register.html", {"request": request})
    except Exception as exc:
        logger.exception(f"An error occurred while rendering the signup page: {exc}")
        return JSONResponse(status_code=500, content={"message": "Server error"})

####################
# signup - POST
####################
@APP.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, username: str = Form(...), email: str = Form(...),
                      password: str = Form(...), cpassword: str = Form(...)):

    # Check if the password and confirm password match
    if password != cpassword:
        return TEMPLATES.TemplateResponse("register.html", {"request": request, "message": "Passwords do not match"})

    # Hash the password
    hashed_password = hash_password(password)

    # Check if a user with the same email already exists
    if SIGNUP_COLLECTION.find_one({"Email": email}):
        return TEMPLATES.TemplateResponse("register.html", {"request": request, "message": "Email already exists"})

    # Create a new user object and insert it into the database
    SIGNUP_COLLECTION.insert_one(User(Username=username, Email=email, Password=hashed_password).dict())

    # Return a success message
    return TEMPLATES.TemplateResponse("register.html", {"request": request, "message": "Registration successful"})

# --------------------------------------------------------------------------
# Logout
# --------------------------------------------------------------------------

@APP.get("/auth/logout", response_class=HTMLResponse)
def logout_get():
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie(SETTING.COOKIE_NAME)
    return response
