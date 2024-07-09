from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(information: str) -> str:
    """Создаем функцию mask_account_card, которая определяет какую информацию пользователь хочет замаскировать и используя
    функции из masks.py маскирует нужные для пользователя данные"""
    user_bank_information = information.split()

    if user_bank_information[0] == "Счет":
        for account in user_bank_information:
            if account.isdigit():
                return user_bank_information[0] + " " + get_mask_account(account)
    else:
        user_card = ""
        for i in user_bank_information:
            if i.isdigit():
                user_card += i
                user_bank_information.remove(i)
        user_bank_information.append(get_mask_card_number(user_card))
        return " ".join(user_bank_information)


def get_date(full_format_date: str) -> str:
    """Создаем функцию get_date, которая преобразует формат даты из 'yyyy-mm-dd' в 'dd.mm.yyyy'"""
    date = full_format_date[:10].split("-")
    dd_mm_yyyy_format_date = ".".join(date[-1::-1])
    return dd_mm_yyyy_format_date


user_input_full_format_date = input("Введите сложный формат даты: ")
print(f"Вот более приятный формат даты: {get_date(user_input_full_format_date)}")

user_input_bank_information = input("\nВведите банковскую информацию, которую нужно замаскировать: ")
print(f"Пожалуйста, замаскированные данные: {mask_account_card(user_input_bank_information)}")
