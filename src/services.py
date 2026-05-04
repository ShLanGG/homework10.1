"""Сервисы: поиск, кешбэк, инвесткопилка"""
import json
import re
import logging
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def simple_search(transactions: List[Dict[str, Any]], search_str: str) -> str:
    """Поиск транзакций по подстроке в описании или категории (регистронезависимо)."""
    if not search_str:
        return json.dumps({"transactions": []}, ensure_ascii=False)
    s_lower = search_str.lower()
    result = [t for t in transactions
              if s_lower in str(t.get("Описание", "")).lower()
              or s_lower in str(t.get("Категория", "")).lower()]
    logger.info(f"Простой поиск '{search_str}': найдено {len(result)}")
    return json.dumps({"transactions": result}, ensure_ascii=False, default=str)

def search_phone_numbers(transactions: List[Dict[str, Any]]) -> str:
    """Ищет транзакции с мобильными номерами в описании."""
    phone_pattern = re.compile(
        r'\+7[-\s]?\d{3}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}|\b8\d{10}\b'
    )
    result = [t for t in transactions
              if phone_pattern.search(str(t.get("Описание", "")))]
    logger.info(f"Найдено {len(result)} транзакций с телефонами")
    return json.dumps({"transactions": result}, ensure_ascii=False, default=str)

def search_person_transfers(transactions: List[Dict[str, Any]]) -> str:
    """Ищет переводы физлицам: категория 'Переводы' и в описании есть 'Имя Ф.'"""
    name_pattern = re.compile(r'\b[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.')
    result = [t for t in transactions
              if t.get("Категория") == "Переводы"
              and name_pattern.search(str(t.get("Описание", "")))]
    logger.info(f"Переводов физлицам: {len(result)}")
    return json.dumps({"transactions": result}, ensure_ascii=False, default=str)

def cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """Анализ выгодных категорий кешбэка: возвращает JSON с суммами возможного кешбэка."""
    cashback = defaultdict(float)
    for t in data:
        # предполагаем формат даты "Дата операции" как datetime или строку
        dt = t.get("Дата операции")
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                continue
        if isinstance(dt, datetime) and dt.year == year and dt.month == month:
            amount = abs(float(t.get("Сумма операции", 0)))
            cashback[t.get("Категория", "Неизвестно")] += amount * 0.01  # 1% кешбэк
    # топ-3 категории по кешбэку
    top3 = sorted(cashback.items(), key=lambda x: x[1], reverse=True)[:3]
    result = {cat: round(val, 2) for cat, val in top3}
    logger.info(f"Кешбэк за {year}-{month:02d}: {result}")
    return json.dumps(result, ensure_ascii=False)

def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Сумма, которая была бы отложена в Инвесткопилку по заданному порогу округления."""
    total = 0.0
    target_month = datetime.strptime(month, "%Y-%m")
    for t in transactions:
        dt = t.get("Дата операции")
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                continue
        if isinstance(dt, datetime) and dt.year == target_month.year and dt.month == target_month.month:
            amount = abs(float(t.get("Сумма операции", 0)))
            # округляем вверх до ближайшего кратного limit
            rounded = ((int(amount) + limit - 1) // limit) * limit
            total += (rounded - amount)
    logger.info(f"Инвесткопилка за {month}: {total:.2f}")
    return round(total, 2)