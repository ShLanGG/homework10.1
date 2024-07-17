def get_mask_card_number(card_number: str) -> str:
    """Маскируем и разбиваем номер карты с помощью f-строки и срезов"""
    card_number_list = card_number.split()
    card_number_without_space = "".join(card_number_list)
    if card_number_without_space.isdigit() is False or len(card_number_without_space) != 16:
        raise ValueError("Длина номера карты только 16 ЦИФР")
    masked_card_number = (
        f"{card_number_without_space[:4]} {card_number_without_space[4:6]}** " f"**** {card_number_without_space[12:]}"
    )
    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Маскируем номер счета с  помощью f-строки с использованием последних 4 чисел номера счета"""
    if len(account_number) < 20 or account_number.isdigit() is not True:
        raise ValueError("Длина счета минимум 20 ЦИФР")
    masked_account_number = f"**{account_number[-4:]}"
    return masked_account_number
