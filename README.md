## Описание
Проект содержит набор функций для обработки списка банковских операций:
- Фильтрация операций по статусу (EXECUTED/CANCELED)
- Сортировка операций по дате
- Маскировка номеров карт и счетов

## Установка и настройка

### Предварительные требования
- **Python**: версия 3.9 или выше
- **Poetry**: менеджер зависимостей (рекомендуется)
- **Git**: для клонирования репозитория

### Пошаговая инструкция по установке

#### 1. Клонирование репозитория
```bash
# SSH
git clone git@github.com:Jeka533/my_project.git


# Переход в директорию проекта
cd my_project
```

### 2. Установи зависимости
```bash
pip install poetry
poetry install
```
### 3. Запуск кода
```bash
poetry shell
python -c "from src.processing import filter_by_state; print('OK')"
```

# Примеры использования
from src.processing import filter_by_state

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27'},
]

### По умолчанию EXECUTED
executed = filter_by_state(operations)
print(executed)

### CANCELED
canceled = filter_by_state(operations, 'CANCELED')
print(canceled)

# Сортировка по дате
from src.processing import sort_by_date

### Сначала новые
new_first = sort_by_date(operations)
print(new_first)

### Сначала старые
old_first = sort_by_date(operations, is_reverse=False)
print(old_first)

# Маскировка
from src.masks import get_mask_card_number, get_mask_account

### Карта: 1234 56** **** 3456
print(get_mask_card_number("1234567890123456"))

### Счет: **7890
print(get_mask_account("1234567890"))

# Контакты
 #### Email evgeniykoval833@mail.ru
 #### GitHub Jeka533