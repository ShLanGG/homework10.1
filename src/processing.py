from datetime import datetime


def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """Создаем функцию filter_by_state, которая принимает на вход список словарей и параметр state(по умолчанию "EXECUTED").
    Функция возвращает новый список словарей, соответствующих параметру state"""
    return [item for item in operations if item.get("state") == state]


def sort_by_date(operations: list, reverse: bool = True) -> list:
    """Создаем функцию sort_by_date, которая принимает на вход список словарей и параметр reverse(по умол. "True").
    Функция возвращает новый список словарей, сортированных по дате операций, согласно параметру reverse"""
    try:
        return sorted(operations, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=reverse)
    except:
        raise ValueError("Есть неккоректная дата(-ы)")
