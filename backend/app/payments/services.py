import requests
import base64
from flask import current_app
from datetime import datetime


# -----------------------------
# 1. GET ACCESS TOKEN
# -----------------------------
def _get_required_config(key):
    value = current_app.config.get(key)
    if not value:
        raise RuntimeError(f"Missing required payment config: {key}")
    return value


def get_access_token():
    consumer_key = _get_required_config("DARAJA_CONSUMER_KEY")
    consumer_secret = _get_required_config("DARAJA_CONSUMER_SECRET")
    base_url = _get_required_config("DARAJA_BASE_URL")

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(url, headers=headers)

    print("----------- TOKEN RESPONSE -----------")
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    data = response.json()

    if "access_token" not in data:
        raise Exception(f"Failed to get access token: {data}")

    return data["access_token"]


# -----------------------------
# 2. GENERATE STK PASSWORD
# -----------------------------
def generate_stk_password():
    shortcode = _get_required_config("DARAJA_SHORTCODE")
    passkey = _get_required_config("DARAJA_PASSKEY")

    print("SHORTCODE:", current_app.config["DARAJA_SHORTCODE"])
    print("PASSKEY:", current_app.config["DARAJA_PASSKEY"])

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    encoded_password = base64.b64encode(data_to_encode.encode()).decode()

    return {
        "timestamp": timestamp,
        "password": encoded_password
    }


# -----------------------------
# 3. INITIATE STK PUSH
# -----------------------------
def initiate_stk_push(phone, amount):

    base_url = _get_required_config("DARAJA_BASE_URL")
    shortcode = _get_required_config("DARAJA_SHORTCODE")
    callback_url = _get_required_config("DARAJA_CALLBACK_URL")

    # Get OAuth token
    access_token = get_access_token()

    # Generate password
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

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=90
    )

    print("----------- STK REQUEST -----------")
    print("URL:", url)
    print("PAYLOAD:", payload)
    print("HEADERS:", headers)

    print("----------- STK RESPONSE -----------")
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    try:
        return response.json()
    except Exception:
        return {
            "error": "Invalid JSON response",
            "status_code": response.status_code,
            "raw_response": response.text
        }