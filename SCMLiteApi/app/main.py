
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.config import SETTING
from route.shipment import shipment, datastream
from route.users import user

load_dotenv()

TEMPLATES = Jinja2Templates(directory="templates")

# Create a FastAPI app instance

APP = FastAPI(title=SETTING.TITLE,\
DESCRIPTION=SETTING.DESCRIPTION, version=SETTING.PROJECT_VERSION)
APP.mount("/static", StaticFiles(directory="static"), name="static")
@APP.exception_handler(HTTPException)
async def redirect_to_signup(request: Request, exc: HTTPException) -> Response:
    if exc.status_code == 401:
        return RedirectResponse('/signup')
    raise exc


APP.include_router(shipment.APP)
APP.include_router(datastream.APP)
APP.include_router(user.APP)
