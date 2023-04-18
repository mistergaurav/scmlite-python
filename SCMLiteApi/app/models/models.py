
from pydantic import BaseModel

class User(BaseModel):
    Username: str
    Email: str
    Password: str

class Shipment(BaseModel):
    Shipment_Invoice_Number: str
    Container_Number: int
    Description: str
    Route_Details: str
    Goods_Type: str
    Device: str
    Expected_Delivery_Date: str
    Po_Number: int
    Delivery_number: int
    NDCNumber: int
    Batch_Id: int
    Serialnumberofgoods: int
    mailid: str
    