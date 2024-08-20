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
    if transaction["operationAmount"]["currency"]["code"] == "RUB":
        return transaction["operationAmount"].get("amount")
    else:
        return get_exchange_amount(
            transaction["operationAmount"]["currency"].get("code"), transaction["operationAmount"].get("amount")
        )
