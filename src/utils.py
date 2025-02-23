import json
import os

from src.external_api import get_exchange_amount


def get_operations(file_path):
    """
    Загружает данные о транзакциях из JSON-файла.

    :param file_path: Абсолютный путь до JSON-файла
    :return: Список словарей с данными о транзакциях или пустой список в случае ошибок.
    """
    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def get_transaction_amount(transaction: dict) -> float:
    try:
        if transaction["operationAmount"]["currency"]["code"] == "RUB":
            amount = transaction["operationAmount"].get("amount")
            return float(amount) if amount is not None else 0.0
        else:
            amount = get_exchange_amount(
                transaction["operationAmount"]["currency"].get("code"), transaction["operationAmount"].get("amount")
            )
            return float(amount) if amount is not None else 0.0
    except (KeyError, TypeError, ValueError) as e:
        print(f"Ошибка при обработке транзакции: {e}")
        return 0.0
