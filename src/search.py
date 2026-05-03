"""
Модуль для поиска транзакций по описанию и подсчёта операций по категориям.
"""
import re
from collections import Counter
from typing import Dict, List


def search_transactions_by_description(transactions: List[dict], search_string: str) -> List[dict]:
    """
    Возвращает список транзакций, в описании которых содержится search_string.

    Поиск выполняется с использованием регулярных выражений (без учёта регистра).
    """
    if not search_string:
        return []
    
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [
        t for t in transactions
        if 'description' in t and pattern.search(str(t['description']))
    ]


def count_transactions_by_categories(transactions: List[dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям.

    Категории сопоставляются по полю 'description' транзакции.
    Используется Counter из collections.
    Возвращает словарь {категория: количество}.
    """
    # Приводим категории к единому регистру для сопоставления
    categories_lower = [cat.lower() for cat in categories]
    # Собираем описания, нормализуя регистр
    descriptions = [
        t.get('description', '').lower() for t in transactions
    ]
    # Подсчитываем только те описания, которые совпадают с одной из категорий
    matched = [desc for desc in descriptions if desc in categories_lower]
    counter = Counter(matched)
    # Возвращаем словарь с изначальным написанием категорий (не lower)
    return {cat: counter.get(cat.lower(), 0) for cat in categories}