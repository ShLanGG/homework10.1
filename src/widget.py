from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(information: str) -> str:
    """Создаем функцию mask_account_card, которая определяет какую информацию пользователь хочет замаскировать и используя
    функции из masks.py, маскируя нужные для пользователя данные"""

    user_bank_information = information.split()

    if user_bank_information[0] == "Счет":
        return user_bank_information[0] + " " + get_mask_account(user_bank_information[-1])
    else:
        user_card = get_mask_card_number(user_bank_information.pop())
        return ' '.join(user_bank_information) + ' ' + user_card


def get_date(full_format_date: str) -> str:
    """Создаем функцию get_date, которая преобразует формат даты из 'yyyy-mm-dd' в 'dd.mm.yyyy'"""
    date = full_format_date[:10].split("-")
    dd_mm_yyyy_format_date = ".".join(date[-1::-1])
    return dd_mm_yyyy_format_date
