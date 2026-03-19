"""
Модуль для маскирования конфиденциальных данных.
"""

from logger_setup import setup_logger

# Настройка логгера для модуля masks
logger = setup_logger(__name__, "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маскированный номер карты.

    Args:
        card_number: Номер карты (16 цифр)

    Returns:
        str: Замаскированный номер карты или сообщение об ошибке
    """
    logger.info(f"Вызов get_mask_card_number с номером: {card_number[:4]}***")

    if len(card_number) != 16 or not card_number.isdigit():
        error_message = "Введен некорректный номер карты"
        logger.error(f"Ошибка валидации: {error_message}")
        return error_message

    result = f"{card_number[0:4]} {card_number[4:6]}** **** {card_number[12:16]}"
    logger.info(f"Успешно замаскирован номер карты: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маскированный номер счета.

    Args:
        account_number: Номер счета (20 цифр)

    Returns:
        str: Замаскированный номер счета или сообщение об ошибке
    """
    logger.info(f"Вызов get_mask_account с номером: {account_number[-4:]}")

    if len(account_number) != 20 or not account_number.isdigit():
        error_message = "Введен некорректный номер счета"
        logger.error(f"Ошибка валидации: {error_message}")
        return error_message

    result = f"**{account_number[-4:]}"
    logger.info(f"Успешно замаскирован номер счета: {result}")
    return result


# Для тестирования
if __name__ == "__main__":
    print(get_mask_card_number(card_number="1234567890123456"))
    print(get_mask_account(account_number="12345678900987654321"))
