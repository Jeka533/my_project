from src.widget import get_date, mask_account_card

print("ПРОВЕРКА РАБОТЫ ФУНКЦИЙ")

# Тестирование mask_account_card
test_data = [
    "Maestro 1596837868705199",
    "Счет 64686473678894779589",
    "MasterCard 7158300734726758",
    "Счет 35383033474447895560",
    "Visa Classic 6831982476737658",
    "Visa Platinum 8990922113665229",
    "Visa Gold 5999414228426353",
    "Счет 73654108430135874305",
]

print("\n1. МАСКИРОВКА КАРТ И СЧЕТОВ:")

for item in test_data:
    result = mask_account_card(item)
    print(f"{item:50}  {result}")

# Тестирование get_date
print("\n2. ПРЕОБРАЗОВАНИЕ ДАТЫ:")

test_dates = ["2024-03-11T02:26:18.671407", "2023-12-31T23:59:59", "2024-01-01T00:00:00", "2024-02-29T15:30:45.123456"]

for date in test_dates:
    result = get_date(date)
    print(f"{date:35}  {result}")
