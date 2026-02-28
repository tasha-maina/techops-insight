import requests
import base64
from flask import current_app
from datetime import datetime



def get_access_token():
    consumer_key = current_app.config["DARAJA_CONSUMER_KEY"]
    consumer_secret = current_app.config["DARAJA_CONSUMER_SECRET"]
    base_url = current_app.config["DARAJA_BASE_URL"]

    # Create base64 credentials
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def generate_stk_password():
    shortcode = current_app.config["DARAJA_SHORTCODE"]
    passkey = current_app.config["DARAJA_PASSKEY"]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    encoded_password = base64.b64encode(data_to_encode.encode()).decode()

    return {
        "timestamp": timestamp,
        "password": encoded_password
    }

def initiate_stk_push(phone, amount):
    base_url = current_app.config["DARAJA_BASE_URL"]
    shortcode = current_app.config["DARAJA_SHORTCODE"]
    callback_url = current_app.config["DARAJA_CALLBACK_URL"]

    # Get access token
    token_response = get_access_token()
    access_token = token_response.get("access_token")

    # Generate password + timestamp
    stk_data = generate_stk_password()
    password = stk_data["password"]
    timestamp = stk_data["timestamp"]

    url = f"{base_url}/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "TechOpsInsight",
        "TransactionDesc": "Payment"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()