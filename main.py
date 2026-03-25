import os
import sys

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(__file__))

print("ЗАПУСК ПРИЛОЖЕНИЯ")

try:
    from src.masks import get_mask_account, get_mask_card_number
    print(" Модуль masks импортирован")
except ImportError as e:
    print(f" Ошибка импорта masks: {e}")

try:
    from scripts.utils import load_transactions
    print(" Модуль utils импортирован")
except ImportError as e:
    print(f" Ошибка импорта utils: {e}")

# Тестируем функции
print("ТЕСТИРОВАНИЕ")

# Тест masks
print("\n1. Тест маскировки карты:")
result = get_mask_card_number("1234567890123456")
print(f"   {result}")

print("\n2. Тест маскировки счета:")
result = get_mask_account("12345678900987654321")
print(f"   {result}")

# Тест utils
print("\n3. Тест загрузки транзакций:")
if os.path.exists("data/operations.json"):
    transactions = load_transactions("data/operations.json")
    print(f"   Загружено транзакций: {len(transactions)}")
else:
    print("   Файл data/operations.json не найден")

print("ПРОВЕРЬТЕ ПАПКУ logs/")
print("Должны быть файлы:")
print("  - logs/masks.log")
print("  - logs/utils.log")
