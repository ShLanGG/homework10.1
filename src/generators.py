def filter_by_currency(transactions: list, currency: str) -> None:
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions):
    for description in transactions:
        yield description.get("description")


def card_number_generator(start, end):
    for num in range(start, end + 1):
        card_number = f'{num:016d}'
        yield f'{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}'
