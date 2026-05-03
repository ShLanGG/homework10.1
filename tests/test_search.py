import pytest
from src.search import search_transactions_by_description, count_transactions_by_categories

test_data = [
    {"description": "Открытие вклада"},
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"},
    {"description": "Оплата услуг"},
    {"description": "Открытие вклада"},
]

def test_search_existing_word():
    result = search_transactions_by_description(test_data, "вклад")
    assert len(result) == 2

def test_search_case_insensitive():
    result = search_transactions_by_description(test_data, "ПЕРЕВОД")
    assert len(result) == 2

def test_search_no_match():
    result = search_transactions_by_description(test_data, "кредит")
    assert result == []

def test_search_empty_string():
    result = search_transactions_by_description(test_data, "")
    assert result == []

def test_count_categories():
    categories = ["Открытие вклада", "Перевод организации", "Оплата услуг", "Несуществующая"]
    counts = count_transactions_by_categories(test_data, categories)
    assert counts == {
        "Открытие вклада": 2,
        "Перевод организации": 1,
        "Оплата услуг": 1,
        "Несуществующая": 0,
    }