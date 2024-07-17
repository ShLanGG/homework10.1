from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(information: str) -> str:
    """Создаем функцию mask_account_card, которая определяет какую информацию пользователь хочет замаскировать и,
    используя функции из masks.py, маскирует нужные для пользователя данные"""

    user_bank_information = information.split()
    user_number = ""
    user_acc_name = []

    for info in user_bank_information:
        if info.isdigit() is True:
            user_number += "".join(info)
        else:
            user_acc_name.append(info)

    if (
        len(user_bank_information) > 1
        and len(user_acc_name) != 0
        and len(user_number) != 0
        and 15 < len(user_number) < 21
    ):
        if user_acc_name[0] == "Счет":
            return user_acc_name[0] + " " + get_mask_account("".join(user_number))
        return " ".join(user_acc_name) + " " + get_mask_card_number(" ".join(user_number))
    raise ValueError("Введены некорректные данные!")


def get_data(full_format_date: str) -> str:
    """Создаем функцию get_date, которая преобразует формат даты из 'yyyy-mm-dd' в 'dd.mm.yyyy'"""
    try:
        date_obj = datetime.fromisoformat(full_format_date[:10])
    except:
        raise ValueError("Введён неправильный формат даты")
    formatted_date = date_obj.strftime("%d.%m.%Y")
    return formatted_date
