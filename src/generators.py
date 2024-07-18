def filter_by_currency(transactions: list, currency: str) -> None:
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions):
    for description in transactions:
        yield description.get("description")

