import requests
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CURRENCY_API_KEY")
BASE_URL = "https://api.currencyapi.com/v3/latest"

def convert_currency(amount, from_currency, to_currency):
    try:
        response = requests.get(BASE_URL, params={
            "apikey": API_KEY,
            "base_currency": from_currency,
            "currencies": to_currency
        })
        response.raise_for_status()
        data = response.json()
        rate = data["data"][to_currency]["value"]
        return round(amount * rate, 2), rate
    except Exception:
        return amount, 1.0