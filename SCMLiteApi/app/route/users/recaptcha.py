import requests
from google.oauth2.credentials import Credentials

def verify_recaptcha(recaptcha_response: str) -> bool:
    credentials = Credentials.from_authorized_user_info(info=None)
    data = {
        "secret": "6LeA0vUkAAAAADOkRTA2hhixEvPmtv-hhX9VaV-Y",
        "response": recaptcha_response
    }
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    return response.json()["success"]
