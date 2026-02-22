from src.masks import get_mask_account, get_mask_card_number

"""Модуль для работы с виджетами."""


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета.
    """
    # Разделяем строку на тип и номер
    parts = account_info.rsplit(" ", 1)

    if len(parts) != 2:
        return "Ошибка: неверный формат данных"

    account_type = parts[0]
    account_number = parts[1]

    # Определяем тип и применяем соответствующую маску
    if account_type.lower() == "счет":
        masked_number = get_mask_account(account_number)
    else:
        masked_number = get_mask_card_number(account_number)

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат "ДД.ММ.ГГГГ".
    """
    if not date_string:
        return "Ошибка: пустая строка"

    # Извлекаем только дату (часть до T)
    date_part = date_string.split("T")[0]

    # Разбиваем дату на компоненты
    date_components = date_part.split("-")

    if len(date_components) != 3:
        return "Ошибка: неверный формат даты"

    year, month, day = date_components

    # Форматируем в нужный вид
    return f"{day}.{month}.{year}"


# Тестирование функций
if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ ФУНКЦИЙ")

    # Тестовые данные для mask_account_card
    test_cards = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    print("\n1. Функция mask_account_card:")

    for test in test_cards:
        result = mask_account_card(test)
        print(f"{test:50}  {result}")

    # Тестовые данные для get_date
    test_dates = [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59",
        "2024-01-01T00:00:00",
        "2024-02-29T15:30:45.123456",
    ]

    print("\n2. Функция get_date:")

    for test in test_dates:
        result = get_date(test)
        print(f"{test:35} -> {result}")
