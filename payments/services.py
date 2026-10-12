
import base64
from datetime import datetime
from decimal import Decimal

import requests
from django.conf import settings


def daraja_base_url():
    environment = getattr(settings, "DARAJA_ENV", "sandbox").lower()

    if environment == "production":
        return "https://api.safaricom.co.ke"

    return "https://sandbox.safaricom.co.ke"


def get_access_token():
    consumer_key = settings.DARAJA_CONSUMER_KEY
    consumer_secret = settings.DARAJA_CONSUMER_SECRET

    response = requests.get(
        f"{daraja_base_url()}/oauth/v1/generate",
        params={"grant_type": "client_credentials"},
        auth=(consumer_key, consumer_secret),
        timeout=30,
    )
    response.raise_for_status()

    token = response.json().get("access_token")
    if not token:
        raise ValueError("Daraja did not return an access token.")

    return token


def initiate_stk_push(
    phone_number,
    amount,
    account_reference,
    transaction_desc,
):
    shortcode = str(settings.DARAJA_SHORTCODE)
    passkey = settings.DARAJA_PASSKEY
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        f"{shortcode}{passkey}{timestamp}".encode("utf-8")
    ).decode("utf-8")

    # Daraja STK Push accepts a whole-number amount.
    amount = int(Decimal(str(amount)).quantize(Decimal("1")))

    if amount < 1:
        raise ValueError("Payment amount must be at least KSh 1.")

    # Normalize common Kenyan mobile number formats.
    phone = "".join(c for c in str(phone_number) if c.isdigit())

    if phone.startswith("0") and len(phone) == 10:
        phone = "254" + phone[1:]
    elif phone.startswith("7") and len(phone) == 9:
        phone = "254" + phone
    elif phone.startswith("1") and len(phone) == 9:
        phone = "254" + phone

    if len(phone) != 12 or not phone.startswith("254"):
        raise ValueError(
            "Enter a valid Kenyan phone number, e.g. 0712345678."
        )

    token = get_access_token()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": settings.DARAJA_CALLBACK_URL,
        "AccountReference": str(account_reference)[:12],
        "TransactionDesc": str(transaction_desc)[:13],
    }

    response = requests.post(
        f"{daraja_base_url()}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("ResponseCode") != "0":
        raise ValueError(
            data.get("ResponseDescription", "STK Push request was rejected.")
        )

    return data
