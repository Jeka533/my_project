def get_mask_card_number() -> str:
    """Функция возвращает маски номера карты"""
    card_number = input("Введите номер карты (16 цифр): ").strip()
    result = ""
    if len(card_number) != 16 or card_number.isdigit() is False:
        result = "Введен некорректный номер карты"
    else:
        result = f"{card_number[0:4]} {card_number[4:6]}** **** {card_number[12:16]}"
    return result


print(get_mask_card_number())
