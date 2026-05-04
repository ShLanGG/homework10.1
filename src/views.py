"""Генерация JSON для веб-страниц"""
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.external_api import get_currency_rates, get_stock_prices
from src.file_reader import get_transactions_list

logger = logging.getLogger(__name__)
USER_SETTINGS_PATH = "user_settings.json"

def load_settings() -> dict:
    try:
        with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки настроек: {e}")
        return {"user_currencies": [], "user_stocks": []}

def get_greeting(dt: datetime) -> str:
    hour = dt.hour
    if 6 <= hour < 12: return "Доброе утро"
    elif 12 <= hour < 18: return "Добрый день"
    elif 18 <= hour < 23: return "Добрый вечер"
    else: return "Доброй ночи"

def get_main_page(date_str: str, file_path="data/operations.xlsx") -> Dict:
    """Главная страница – приветствие, карты, топ-5, валюты, акции."""
    target = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    transactions = get_transactions_list(file_path)
    # фильтр по дате: с начала месяца до target
    start = target.replace(day=1, hour=0, minute=0, second=0)
    transactions = [t for t in transactions
                    if parser_date(t.get("Дата операции")) and start <= parser_date(t["Дата операции"]) <= target]

    greeting = get_greeting(target)
    cards = {}
    for t in transactions:
        card = str(t.get("Номер карты", "")).replace("*", "")
        digits = card[-4:] if len(card) >= 4 else "0000"
        amount = float(t.get("Сумма платежа", 0))
        cards.setdefault(digits, {"total_spent": 0.0, "cashback": 0.0})
        cards[digits]["total_spent"] += amount
        cards[digits]["cashback"] += amount / 100.0

    top_trans = sorted(transactions, key=lambda x: float(x.get("Сумма платежа", 0)), reverse=True)[:5]
    top5 = []
    for t in top_trans:
        dt = parser_date(t.get("Дата операции"))
        top5.append({
            "date": dt.strftime("%d.%m.%Y") if dt else "",
            "amount": float(t.get("Сумма платежа", 0)),
            "category": t.get("Категория", ""),
            "description": t.get("Описание", "")
        })

    settings = load_settings()
    cur_rates = get_currency_rates(settings.get("user_currencies", []))
    st_prices = get_stock_prices(settings.get("user_stocks", []))
    return {
        "greeting": greeting,
        "cards": [{"last_digits": k, "total_spent": round(v["total_spent"], 2),
                   "cashback": round(v["cashback"], 2)} for k, v in cards.items()],
        "top_transactions": top5,
        "currency_rates": cur_rates,
        "stock_prices": st_prices
    }

def get_events_page(date_str: str, range_type: str = "M", file_path="data/operations.xlsx") -> Dict:
    """Страница События – расходы, поступления, курсы, акции."""
    target = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    if range_type == "W":
        start = target - timedelta(days=target.weekday())  # начало недели
        start = start.replace(hour=0, minute=0, second=0)
    elif range_type == "M":
        start = target.replace(day=1, hour=0, minute=0, second=0)
    elif range_type == "Y":
        start = target.replace(month=1, day=1, hour=0, minute=0, second=0)
    else:  # ALL
        start = datetime(2000, 1, 1)
    
    transactions = get_transactions_list(file_path)
    filtered = []
    for t in transactions:
        dt = parser_date(t.get("Дата операции"))
        if dt and start <= dt <= target:
            filtered.append(t)

    expenses = []   # сумма < 0
    income = []     # сумма > 0
    for t in filtered:
        s = float(t.get("Сумма операции", 0))
        if s < 0:
            expenses.append(t)
        elif s > 0:
            income.append(t)

    # Расходы
    total_expense = round(sum(abs(float(t["Сумма операции"])) for t in expenses))
    cat_exp = {}
    transfers_cash = []
    for t in expenses:
        cat = t.get("Категория", "")
        amt = abs(float(t["Сумма операции"]))
        if cat in ("Наличные", "Переводы"):
            transfers_cash.append((cat, amt))
        else:
            cat_exp[cat] = cat_exp.get(cat, 0) + amt

    sorted_main = sorted(cat_exp.items(), key=lambda x: x[1], reverse=True)
    top7 = sorted_main[:7]
    other = sum(v for _, v in sorted_main[7:])
    main_list = [{"category": c, "amount": round(v)} for c, v in top7]
    if other > 0:
        main_list.append({"category": "Остальное", "amount": round(other)})

    # Группируем наличные и переводы
    tc_dict = {}
    for cat, amt in transfers_cash:
        tc_dict[cat] = tc_dict.get(cat, 0) + amt
    tc_list = [{"category": c, "amount": round(a)} for c, a in
               sorted(tc_dict.items(), key=lambda x: x[1], reverse=True)]

    # Поступления
    total_income = round(sum(float(t["Сумма операции"]) for t in income))
    inc_cat = {}
    for t in income:
        cat = t.get("Категория", "")
        inc_cat[cat] = inc_cat.get(cat, 0) + float(t["Сумма операции"])
    inc_main = [{"category": c, "amount": round(a)} for c, a in
                sorted(inc_cat.items(), key=lambda x: x[1], reverse=True)]

    settings = load_settings()
    cur_rates = get_currency_rates(settings.get("user_currencies", []))
    st_prices = get_stock_prices(settings.get("user_stocks", []))

    return {
        "expenses": {
            "total_amount": total_expense,
            "main": main_list,
            "transfers_and_cash": tc_list
        },
        "income": {
            "total_amount": total_income,
            "main": inc_main
        },
        "currency_rates": cur_rates,
        "stock_prices": st_prices
    }

def parser_date(date_val) -> Optional[datetime]:
    if isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, str):
        for fmt in ("%d.%m.%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(date_val, fmt)
            except ValueError:
                pass
    return None