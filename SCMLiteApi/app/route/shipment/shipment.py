
from fastapi import Form, Request, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.config import SETTING
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from fastapi.responses import HTMLResponse
from models.models import Shipment
from models.models import User
from route.users.user_authentication import get_current_user_from_token, get_current_user_from_cookie


load_dotenv()

APP = APIRouter(tags=["creating shipment api's"])

APP.mount("/static", StaticFiles(directory="static"), name="static")

TEMPLATES = Jinja2Templates(directory="templates")

CLIENT = SETTING.CLIENT

SHIPMENT_COLLECTION = SETTING.SHIPMENT_COLLECTION

SHIPMENT_TEMPLATE = "shipment.html"

######################################################################
# Create Shipment Page GET
######################################################################
# Create shipment page that only logged in users can access.


@APP.get("/shipment", response_class=HTMLResponse)
def get_shipment_page(request: Request, user: User = Depends(get_current_user_from_token)):
    try:
        return TEMPLATES.TemplateResponse(SHIPMENT_TEMPLATE, {"user": user, "request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

######################################################################
# shipment POST
######################################################################



@APP.post("/shipment", response_class=HTMLResponse)
def post_shipment_page(request: Request, shipment_invoice_number: str = Form(...), container_number: int = Form(...),
                       description: str = Form(...), route_details: str = Form(...), goods_type: str = Form(...),
                       device: str = Form(...), delivery_date: str = Form(...), po_number: int = Form(...),
                       delivery_number: int = Form(...), ndcnumber: int = Form(...), batch_id: int = Form(...),
                       serialnumberofgoods: int = Form(...)):
    try:
        # Get the current user from the cookie and create a new Shipment object
        user_name = get_current_user_from_cookie(request)
        user = Shipment(Shipment_Invoice_Number=shipment_invoice_number, Container_Number=container_number,
                        Description=description, Route_Details=route_details, Goods_Type=goods_type,
                        Device=device, Expected_Delivery_Date=delivery_date, Po_Number=po_number,
                        Delivery_number=delivery_number, NDCNumber=ndcnumber, Batch_Id=batch_id,
                        Serialnumberofgoods=serialnumberofgoods, mailid=user_name["Email"])

        # Check if the shipment invoice number already exists in the database
        data = SHIPMENT_COLLECTION.find_one({"Shipment_Invoice_Number": shipment_invoice_number})
        if data:
            # If it does, return an error message
            context = {"request": request, "user": user_name, "message": "*Shipment_Invoice_Number already exists",
                       "delivery_date": delivery_date, "goods_type": goods_type}
        else:
            # If it doesn't, insert the new shipment into the database and return a success message
            SHIPMENT_COLLECTION.insert_one(user.dict())
            context = {"request": request, "user": user_name, "success_message": "Success! Your shipment has been created",
                       "delivery_date": delivery_date, "goods_type": goods_type}
        return TEMPLATES.TemplateResponse(SHIPMENT_TEMPLATE, context)
    except ValueError as exc:
        # If there is an issue with the input values, raise a 422 Unprocessable Entity error message
        raise HTTPException(status_code=422, detail="Unprocessable Entity , Please check your input values.") from exc
    except PyMongoError as exc:
        # If there is an issue with the database, raise a 500 Internal Server Error message
        raise HTTPException(status_code=500, detail="Database error. Please try again later.") from exc
    except Exception as exc:
        # If there is any other kind of exception, raise a 500 Internal Server Error message
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(exc)}") from exc

######################################################################
# show shipment -GET
######################################################################


@APP.get("/show-shipment", response_class=HTMLResponse)
def get_created_shipments(request: Request, user: User = Depends(get_current_user_from_token)):
    try:
        shipment_user = get_current_user_from_cookie(request)
        shipment_data = list(SHIPMENT_COLLECTION.find({"mailid": shipment_user["Email"]}, {'_id': 0}))
        if shipment_data:
            value = shipment_data[-1]["Route_Details"]
            delivery_from, delivery_to = value.split()[0], value.split()[-1]
            return TEMPLATES.TemplateResponse("shipmentList.html", {"shipment_user": shipment_user, "shipment_data": shipment_data, "request": request, "user": user, "delivery_from": delivery_from, "delivery_to": delivery_to})
        else:
            return TEMPLATES.TemplateResponse("newShipments.html", {"shipment_user": shipment_user, "request": request, "shipment": " You don't have any Shipments, try creating new one."})
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
