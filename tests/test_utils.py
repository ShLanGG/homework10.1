from unittest.mock import mock_open, patch
from src.utils import get_operations, get_transaction_amount

# Пример данных для транзакции в рублях и долларах
rub_transaction = {
    "operationAmount": {
        "amount": 1000,
        "currency": {
            "code": "RUB"
        }
    }
}

usd_transaction = {
    "operationAmount": {
        "amount": 100,
        "currency": {
            "code": "USD"
        }
    }
}

eur_transaction = {
    "operationAmount": {
        "amount": 100,
        "currency": {
            "code": "EUR"
        }
    }
}


def mock_get_exchange_amount(currency_code, amount):
    if currency_code == "USD":
        return amount * 74.0  # Пример курса USD -> RUB
    elif currency_code == "EUR":
        return amount * 85.0  # Пример курса EUR -> RUB
    return amount


@patch('builtins.open', new_callable=mock_open, read_data='[{"amount": 1000}]')
@patch('os.path.isfile', return_value=True)
def test_get_operations_valid(mock_isfile, mock_file):
    result = get_operations('/fake/path/operations.json')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["amount"] == 1000


@patch('builtins.open', new_callable=mock_open, read_data='{"invalid": "data"}')
@patch('os.path.isfile', return_value=True)
def test_get_operations_invalid_format(mock_isfile, mock_file):
    result = get_operations('/fake/path/operations.json')
    assert result == []


@patch('os.path.isfile', return_value=False)
def test_get_operations_file_not_found(mock_isfile):
    result = get_operations('/fake/path/operations.json')
    assert result == []


@patch('src.utils.get_exchange_amount', side_effect=mock_get_exchange_amount)
def test_get_transaction_amount_eur(mock_exchange):
    assert get_transaction_amount(eur_transaction) == 100 * 85.0


@patch('src.utils.get_exchange_amount', side_effect=mock_get_exchange_amount)
def test_get_transaction_amount_usd(mock_exchange):
    assert get_transaction_amount(usd_transaction) == 100 * 74.0


def test_get_transaction_amount_rub():
    assert get_transaction_amount(rub_transaction) == 1000
