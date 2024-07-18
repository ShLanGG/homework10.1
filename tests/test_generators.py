import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.mark.parametrize('currency, expected', [
    ('EUR', [{"id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "EUR",
                      "code": "EUR"
                  }
              },
              "description": "Перевод с карты на карту",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
              }]),
    ('USD', [{"id": 939719570,
              "state": "EXECUTED",
              "date": "2018-06-30T02:08:58.425572",
              "operationAmount": {
                  "amount": "9824.07",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод организации",
              "from": "Счет 75106830613657916952",
              "to": "Счет 11776614605963066702"
              }]),
    ('RUB', [{"id": 1234556789,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "RUB",
                      "code": "RUB"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
              }]),
    ('CYN', []),
])
def test_filter_by_currency(list_of_transactions, currency, expected):
    result = list(filter_by_currency(list_of_transactions, currency))
    assert result == expected


@pytest.mark.parametrize('currency', ['EUR', 'USD'])
def test_filter_by_currency_empty_list(currency, empty_list=None):
    if empty_list is None:
        empty_list = []
    result = list(filter_by_currency(empty_list, currency))
    assert result == []


@pytest.mark.parametrize('expected_result', [
    ['Перевод организации',
     "Перевод с карты на карту",
     "Перевод со счета на счет"]
])
def test_transaction_descriptions(list_of_transactions, expected_result):
    result = list(transaction_descriptions(list_of_transactions))
    assert result == expected_result


@pytest.mark.parametrize('start, stop, expected', [
    (9999999999999999, 10000000000000000, '9999 9999 9999 9999')
])
def test_card_number_generator_max_number(start, stop, expected):
    generator = card_number_generator(start, stop)
    assert next(generator) == expected


def test_card_number_generator(start=1, stop=5):
    generator = card_number_generator(start, stop)
    assert next(generator) == '0000 0000 0000 0001'
    assert next(generator) == '0000 0000 0000 0002'
    assert next(generator) == '0000 0000 0000 0003'
    assert next(generator) == '0000 0000 0000 0004'
    assert next(generator) == '0000 0000 0000 0005'
