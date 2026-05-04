import json
from src.services import simple_search, search_phone_numbers, search_person_transfers, cashback_categories, investment_bank

def test_simple_search_found():
    txns = [{"Описание": "МТС оплата", "Категория": "Связь"}, {"Описание": "Кино", "Категория": "Развлечения"}]
    res = json.loads(simple_search(txns, "мтс"))
    assert len(res["transactions"]) == 1

def test_search_phone_numbers():
    txns = [{"Описание": "Я МТС +7 921 11-22-33"}, {"Описание": "Нет номера"}]
    res = json.loads(search_phone_numbers(txns))
    assert len(res["transactions"]) == 1

def test_search_person_transfers():
    txns = [
        {"Категория": "Переводы", "Описание": "Иван И."},
        {"Категория": "Переводы", "Описание": "Оплата услуг"}
    ]
    res = json.loads(search_person_transfers(txns))
    assert len(res["transactions"]) == 1

def test_cashback_categories():
    from datetime import datetime
    txns = [
        {"Дата операции": datetime(2023, 3, 10), "Сумма операции": -2000, "Категория": "Супермаркеты"},
        {"Дата операции": datetime(2023, 3, 12), "Сумма операции": -500, "Категория": "Транспорт"},
        {"Дата операции": datetime(2023, 3, 15), "Сумма операции": -1200, "Категория": "Супермаркеты"}
    ]
    res = cashback_categories(txns, 2023, 3)
    data = json.loads(res)
    assert "Супермаркеты" in data
    assert data["Супермаркеты"] == 32.0

def test_investment_bank():
    txns = [
        {"Дата операции": "10.03.2023 12:00:00", "Сумма операции": 1712},
        {"Дата операции": "15.03.2023 12:00:00", "Сумма операции": 1234}
    ]
    assert investment_bank("2023-03", txns, 50) == 38 + 16  # 1750-1712=38, 1250-1234=16