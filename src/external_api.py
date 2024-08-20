import os

import requests
from dotenv import load_dotenv


def get_exchange_amount(currency: str, amount: str) -> float:
    """Получает текущий курс валюты к рублю и конвертирует сумму в рубли по текущему курсу"""
    load_dotenv()

    api_key = os.getenv("API_KEY")

    url = "https://api.apilayer.com/exchangerates_data/convert"

    payload = {"amount": amount, "from": currency, "to": "RUB"}
    headers = {"apikey": api_key}

    response = requests.request("GET", url, headers=headers, params=payload)

    result = response.json().get("result")

    return result
