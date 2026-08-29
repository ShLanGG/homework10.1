import os

import requests
from dotenv import load_dotenv

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


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


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Возвращает курсы заданных валют к рублю через API apilayer."""
    import os, requests
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API_KEY не найден")
        return []
    symbols = ",".join(currencies)
    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {"base": "RUB", "symbols": symbols}
    headers = {"apikey": api_key}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        rates = resp.json().get("rates", {})
    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return []
    return [{"currency": c, "rate": rates.get(c, 0.0)} for c in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Возвращает цены акций (пока мок, можно заменить на реальный API)."""
    mock = {"AAPL": 178.0, "AMZN": 135.0, "GOOGL": 142.0, "MSFT": 380.0, "TSLA": 210.0}
    res = []
    for s in stocks:
        price = mock.get(s, 0.0)
        res.append({"stock": s, "price": price})
    return res
