# Home Evaluator 🏠

**Home Evaluator** - це система для оцінки будинків за різними факторами, яка допомагає прийняти рішення при виборі житла. Програма враховує ціну, площу, наявність комунікацій, стан будинку, розташування та інші важливі характеристики.

## 🎯 Основна ідея

Кожен будинок має свої плюси і мінуси:
- Дешевий будинок може не мати необхідних комунікацій
- Дорогий будинок може мати все, але бути занадто дорогим
- Будинок у гарному місці може коштувати дорожче

Ця програма допомагає зважити всі "за" і "проти" та отримати фінальний бал від 0 до 100 для кожного будинку.

## ✨ Функціонал

- ✅ Оцінка будинків за 15+ різними факторами
- ✅ Гнучка система вагових коефіцієнтів
- ✅ Порівняння декількох будинків
- ✅ Детальний розрахунок балів
- ✅ Збереження та завантаження даних
- ✅ Робота з JSON файлами

## 📦 Встановлення

```bash
# Клонувати репозиторій
git clone https://github.com/dmytr0/HomeEvaluator.git
cd HomeEvaluator

# Встановлення залежностей (якщо потрібно)
pip install -r requirements.txt
```

## 🚀 Швидкий старт

### 1. Запуск прикладу

```bash
python home_evaluator.py
```

Це запустить оцінку декількох прикладних будинків і покаже результати.

### 2. Використання у власному коді

```python
from home_evaluator import HomeEvaluator, House

# Створюємо будинок
house = House(
    name="Мій будинок",
    price=100000,
    area=120,
    has_gas=True,
    has_water=True,
    has_sewer=True,
    has_electricity=True,
    has_heating=True,
    has_bathroom=True,
    condition="good",
    location_rating=7
)

# Оцінюємо
evaluator = HomeEvaluator()
result = evaluator.evaluate_house(house)

print(f"Фінальний бал: {result['final_score']:.2f}/100")
```

## 📊 Фактори оцінки

| Фактор | Опис | Вага за замовчуванням |
|--------|------|---------------------|
| **price** | Ціна будинку (нижча - краще) | 15 |
| **area** | Площа будинку (більша - краще) | 10 |
| **has_gas** | Наявність газу | 8 |
| **has_water** | Наявність води | 8 |
| **has_sewer** | Наявність каналізації | 7 |
| **has_electricity** | Наявність електрики | 5 |
| **has_heating** | Наявність опалення | 10 |
| **has_bathroom** | Наявність ванної кімнати | 10 |
| **has_kitchen** | Наявність кухні | 5 |
| **condition** | Стан будинку | 10 |
| **location_rating** | Оцінка розташування (1-10) | 10 |
| **year_built** | Рік побудови | 5 |
| **floors** | Кількість поверхів | 2 |
| **has_garden** | Наявність саду | 2 |
| **has_garage** | Наявність гаражу | 3 |
| **distance_to_city** | Відстань до міста | 5 |

## 🎛️ Налаштування ваг

Ви можете змінити вагові коефіцієнти для різних факторів:

```python
from home_evaluator import HomeEvaluator, EvaluationWeights

# Створюємо власні ваги
custom_weights = EvaluationWeights(
    price_weight=20.0,      # Ціна важливіша
    area_weight=15.0,       # Площа важливіша
    condition_weight=15.0,  # Стан важливіший
    location_weight=15.0   # Розташування важливіше
)

# Використовуємо власні ваги
evaluator = HomeEvaluator(custom_weights)
```

## 📁 Робота з файлами

### Завантаження будинків з JSON

```python
import json
from home_evaluator import HomeEvaluator, House

with open('houses.json', 'r') as f:
    houses_data = json.load(f)

houses = [House.from_dict(data) for data in houses_data]

evaluator = HomeEvaluator()
results = evaluator.compare_houses(houses)
```

### Збереження вагових коефіцієнтів

```python
evaluator = HomeEvaluator(custom_weights)
evaluator.save_weights('my_weights.json')

# Завантаження
evaluator.load_weights('my_weights.json')
```

## 📈 Порівняння будинків

```python
houses = [...]  # Список будинків

evaluator = HomeEvaluator()
results = evaluator.compare_houses(houses, sort_by="final_score")

for result in results:
    print(f"{result['house_name']}: {result['final_score']:.2f} балів")
```

## 🏗️ Структура проєкта

```
HomeEvaluator/
├── home_evaluator.py    # Основний модуль оцінки
├── example_usage.py     # Приклади використання
├── data/
│   └── houses.json      # Прикладні дані будинків
├── README.md            # Документація
└── requirements.txt     # Залежності
```

## 🔧 Доступні стани будинку

- `"excellent"` - Відмінний стан
- `"good"` - Хороший стан
- `"average"` - Середній стан
- `"old"` - Старий стан

## 📝 Приклад виводу

```
ОЦІНКА БУДИНКІВ
================================================================================

1. Будинок 2: Дорогий, але з усіма
   Фінальний бал: 85.42/100
   Ціна: $200,000
   Площа: 150 м²

2. Будинок 7: Елітний котедж
   Фінальний бал: 82.15/100
   Ціна: $300,000
   Площа: 250 м²

3. Будинок 3: Середній варіант
   Фінальний бал: 78.57/100
   Ціна: $100,000
   Площа: 120 м²
...
```

## 🛠️ Налаштування

Ви можете змінити базові значення для нормалізації у класі `HomeEvaluator`:

```python
HomeEvaluator.REFERENCE_PRICE = 150000  # Базова ціна
HomeEvaluator.REFERENCE_AREA = 120      # Базова площа
HomeEvaluator.REFERENCE_YEAR = 2010     # Базовий рік
HomeEvaluator.MAX_DISTANCE = 100        # Максимальна відстань
```

## 💡 Поради

1. **Налаштуйте ваги** під свої пріоритети (наприклад, якщо ціна найважливіша)
2. **Порівнюйте** декілька будинків одночасно
3. **Аналізуйте** детальний розрахунок для розуміння оцінки
4. **Зберігайте** свої ваги для майбутнього використання

## 🤝 Внесок

Якщо у вас є ідеї щодо покращення, створюйте Pull Request!

## 📄 Лічензія

MIT License
