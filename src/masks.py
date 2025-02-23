import logging

# Создание отдельного логера для модуля masks
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

# Настройка file_handler для записи логов в файл
file_handler = logging.FileHandler("logs/masks.log", mode="w")
file_handler.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

# Настройка форматера для логов
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавление handler к логеру
masks_logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты."""
    try:
        card_number_list = card_number.split()
        card_number_without_space = "".join(card_number_list)
        if card_number_without_space.isdigit() is False or len(card_number_without_space) != 16:
            raise ValueError("Длина номера карты только 16 ЦИФР")
        masked_card_number = (
            f"{card_number_without_space[:4]} {card_number_without_space[4:6]}** " f"**** {card_number_without_space[12:]}"
        )
        masks_logger.info(f"Успешно замаскирован номер карты: {card_number}")
        return masked_card_number
    except ValueError as e:
        masks_logger.error(f"Ошибка при маскировании номера карты: {e}", exc_info=True)
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета."""
    try:
        if len(account_number) < 20 or account_number.isdigit() is not True:
            raise ValueError("Длина счета минимум 20 ЦИФР")
        masked_account_number = f"**{account_number[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер счета: {account_number}")
        return masked_account_number
    except ValueError as e:
        masks_logger.error(f"Ошибка при маскировании номера счета: {e}", exc_info=True)
        raise
