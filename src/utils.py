import json
import os
import logging
from src.external_api import get_exchange_amount

# Создание отдельного логера для модуля utils
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

# Создание папки logs, если она не существует
if not os.path.exists("logs"):
    os.makedirs("logs")

# Настройка file_handler для записи логов в файл
file_handler = logging.FileHandler("logs/utils.log", mode="w")
file_handler.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

# Настройка форматера для логов
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавление handler к логеру
utils_logger.addHandler(file_handler)


def get_operations(file_path):
    """
    Загружает данные о транзакциях из JSON-файла.

    :param file_path: Абсолютный путь до JSON-файла
    :return: Список словарей с данными о транзакциях или пустой список в случае ошибок.
    """
    if not os.path.isfile(file_path):
        utils_logger.warning(f"Файл {file_path} не найден.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                utils_logger.info(f"Успешно загружены данные из файла {file_path}.")
                return data
            else:
                utils_logger.warning(f"Файл {file_path} содержит некорректные данные.")
                return []
    except (json.JSONDecodeError, OSError) as e:
        utils_logger.error(f"Ошибка при чтении файла {file_path}: {e}", exc_info=True)
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
        utils_logger.error(f"Ошибка при обработке транзакции: {e}", exc_info=True)
        return 0.0
