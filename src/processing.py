def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """Создаем функцию filter_by_state, которая принимает на вход список словарей и параметр state(по умолчанию "EXECUTED").
    Функция возвращает новый список словарей, соответствующих параметру state"""
    return [item for item in operations if item.get("state") == state]
