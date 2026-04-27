import pandas as pd


def read_csv_file(file_path: str) -> list[dict]:
    """
    Считывает финансовые операции из CSV-файла.

    :param file_path: Путь к CSV-файлу.
    :return: Список словарей с транзакциями.
    """
    try:
        data = pd.read_csv(file_path)
        return data.to_dict("records")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV-файла: {e}")


def read_excel_file(file_path: str) -> list[dict]:
    """
    Считывает финансовые операции из Excel-файла.

    :param file_path: Путь к Excel-файлу.
    :return: Список словарей с транзакциями.
    """
    try:
        data = pd.read_excel(file_path)
        return data.to_dict("records")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла: {e}")