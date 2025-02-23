def filter_by_currency(transactions: list, currency: str):
    """Создаем функцию filter_by_currency, принимающую на вход список словарей и возвращающую итератор,
    который поочередно выдает транзакции, где валюта операции соответствует заданной"""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: list):
    """Создаём генератор, возвращающий описание каждой транзакции, принимая список словарей"""
    for description in transactions:
        yield description.get("description")


def card_number_generator(start, stop):
    """Создаём генератор номеров карт, который принимает определенный диапазон для генерации номеров"""
    if 0 < start < 10**16 or 2 < stop < 10**16 + 1:
        for num in range(start, stop + 1):
            card_number = f"{num:016d}"
            yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
    raise ValueError("Число выходит из диапазона от 1 до 10^16")
