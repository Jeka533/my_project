def get_mask_account() -> str:
    """Функция возвращает маски номера счета"""
    card_number = input("Введите номер лицевого счета (20 цифр): ").strip()
    result = ""
    if len(card_number) != 20 or card_number.isdigit() is False:
        result = "Введен некорректный номер счета"
    else:
        result = f"**{card_number[-4:]}"
    return result


print(get_mask_account())
