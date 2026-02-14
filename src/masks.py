
def get_mask_card_number(card_number: str) -> str:
    """Функция возвращает маски номера карты"""
    result = ""
    if len(card_number) != 16 or card_number.isdigit() is False:
        result = "Введен некорректный номер карты"
    else:
        result = f"{card_number[0:4]} {card_number[4:6]}** **** {card_number[12:16]}"
    return result


print(get_mask_card_number(card_number="1234567890123456"))


def get_mask_account(account_number: str) -> str:
    """Функция возвращает маски номера счета"""
    result = ""
    if len(account_number) != 20 or account_number.isdigit() is False:
        result = "Введен некорректный номер счета"
    else:
        result = f"**{account_number[-4:]}"
    return result


print(get_mask_account(account_number="12345678900987654321"))

