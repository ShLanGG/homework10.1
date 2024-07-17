from src.widget import get_data
def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """Создаем функцию filter_by_state, которая принимает на вход список словарей и параметр state(по умолчанию "EXECUTED").
    Функция возвращает новый список словарей, соответствующих параметру state"""
    return [item for item in operations if item.get("state") == state]


def sort_by_date(operations: list, reverse: bool = True) -> list:
    """Создаем функцию sort_by_date, которая принимает на вход список словарей и параметр reverse(по умол. "True").
    Функция возвращает новый список словарей, сортированных по дате операций, согласно параметру reverse"""
    return sorted(operations, key=lambda x: get_data(x['date']), reverse=reverse)
