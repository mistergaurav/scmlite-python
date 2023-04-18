from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.config import SETTING
from pymongo.errors import PyMongoError  
import logging  
from models.models import User
from route.users.user_authentication import get_current_user_from_token

load_dotenv()

APP = APIRouter(tags=["creating shipment api's"])
APP.mount("/static", StaticFiles(directory="static"), name="static")
TEMPLATES = Jinja2Templates(directory="templates")
CLIENT = SETTING.CLIENT
DATA_STREAM = SETTING.DATA_STREAM

@APP.get("/datastream", response_class=HTMLResponse)
def stream_page(request: Request, user: User = Depends(get_current_user_from_token)):
    try:
        if not request or not user:
            raise HTTPException(status_code=400, detail="Invalid request or user")

        streaming_data = list(DATA_STREAM.find({}))  # Update with appropriate query filter
        if not streaming_data:
            raise HTTPException(status_code=404, detail="No data found in the database")

        return TEMPLATES.TemplateResponse("datastream.html", {"user": user, "streaming_data": streaming_data, "request": request})
    except pymongo.errors.PyMongoError as e:  # Update with appropriate database library exception
        logging.error(f"Error occurred while querying the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve data from the database")
    except HTTPException as he:
        raise he  # Reraise HTTPException to propagate to FastAPI's error handling
    except Exception as e:
        logging.error(f"Unhandled error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
