from scripts.utils import load_transactions

# Загружаем транзакции
transactions = load_transactions("data/operations.json")

# Смотрим, что получилось
if transactions:
    print("\nПервые 3 транзакции:")
    print("-" * 40)

    # Покажем первые 3 транзакции
    for i in range(min(3, len(transactions))):
        t = transactions[i]
        print(f"\nТранзакция {i + 1}:")
        print(f"  ID: {t.get('id')}")
        print(f"  Дата: {t.get('date')}")
        print(f"  Описание: {t.get('description')}")

        # Достаем информацию о сумме
        amount = t.get("operationAmount", {})
        if amount:
            print(f"  Сумма: {amount.get('amount')} {amount.get('currency', {}).get('name')}")
else:
    print("Не удалось загрузить транзакции")
