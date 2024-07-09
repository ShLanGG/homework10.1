def get_mask_card_number(card_number: str) -> str:
    """Маскируем и разбиваем номер карты с помощью f-строки и срезов"""
    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Маскируем номер счета с  помощью f-строки с использованием последних 4 чисел номера счета"""
    masked_account_number = f"**{account_number[-4:]}"
    return masked_account_number
