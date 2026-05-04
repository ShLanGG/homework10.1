import pytest, json, datetime
from unittest.mock import patch, mock_open
from src.views import get_main_page, get_events_page

@patch("src.views.get_transactions_list")
@patch("src.views.load_settings")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_main_page(mock_stock, mock_curr, mock_set, mock_load):
    mock_load.return_value = [
        {"Дата операции": "01.02.2023 12:00:00", "Сумма платежа": 1000, "Номер карты": "*1234",
         "Категория": "Еда", "Описание": "Магазин", "Сумма операции": -1000},
        {"Дата операции": "05.02.2023 10:00:00", "Сумма платежа": 2000, "Номер карты": "*5678",
         "Категория": "ЖКХ", "Описание": "Квартплата", "Сумма операции": -2000}
    ]
    mock_set.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_curr.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_stock.return_value = [{"stock": "AAPL", "price": 150.0}]
    result = get_main_page("2023-02-10 13:00:00")
    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) >= 1
    assert result["top_transactions"][0]["amount"] == 2000

@patch("src.views.get_transactions_list")
@patch("src.views.load_settings")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_events_page(mock_stock, mock_curr, mock_set, mock_load):
    mock_load.return_value = [
        {"Дата операции": "15.03.2023 09:00:00", "Сумма операции": -500, "Категория": "Супермаркеты"},
        {"Дата операции": "16.03.2023 09:00:00", "Сумма операции": -1500, "Категория": "Супермаркеты"},
        {"Дата операции": "17.03.2023 09:00:00", "Сумма операции": -200, "Категория": "Наличные"},
        {"Дата операции": "18.03.2023 09:00:00", "Сумма операции": 3000, "Категория": "Зарплата"}
    ]
    mock_set.return_value = {"user_currencies": ["EUR"], "user_stocks": []}
    mock_curr.return_value = [{"currency": "EUR", "rate": 90.0}]
    mock_stock.return_value = []
    result = get_events_page("2023-03-20 10:00:00", "M")
    assert result["expenses"]["total_amount"] == 2200
    assert len(result["expenses"]["main"]) > 0
    assert result["expenses"]["transfers_and_cash"][0]["category"] == "Наличные"
    assert result["income"]["total_amount"] == 3000