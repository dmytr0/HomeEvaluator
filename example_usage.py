#!/usr/bin/env python3
"""
Приклади використання Home Evaluator
"""

import json
from home_evaluator import HomeEvaluator, House, EvaluationWeights


def example_basic_usage():
    """Базовий приклад використання"""
    print("=" * 80)
    print("ПРИКЛАД 1: Базова оцінка будинку")
    print("=" * 80)
    
    # Створюємо будинок
    my_house = House(
        name="Мій будинок",
        price=80000,
        area=110,
        has_gas=True,
        has_water=True,
        has_sewer=True,
        has_electricity=True,
        has_heating=True,
        has_bathroom=True,
        has_kitchen=True,
        condition="good",
        location_rating=7,
        year_built=2000,
        floors=1,
        has_garden=True,
        has_garage=False,
        distance_to_city=5
    )
    
    # Створюємо евалюатор
    evaluator = HomeEvaluator()
    
    # Оцінюємо будинок
    result = evaluator.evaluate_house(my_house)
    
    print(f"Будинок: {result['house_name']}")
    print(f"Фінальний бал: {result['final_score']:.2f}/100")
    print()


def example_compare_houses():
    """Порівняння декількох будинків"""
    print("=" * 80)
    print("ПРИКЛАД 2: Порівняння будинків")
    print("=" * 80)
    
    # Створюємо декілька будинків
    houses = [
        House(
            name="Варіант А: Дешевий",
            price=50000,
            area=80,
            has_gas=False,
            has_water=True,
            has_electricity=True,
            condition="old",
            location_rating=5
        ),
        House(
            name="Варіант Б: Середній",
            price=100000,
            area=120,
            has_gas=True,
            has_water=True,
            has_sewer=True,
            has_electricity=True,
            has_heating=True,
            condition="good",
            location_rating=7
        ),
        House(
            name="Варіант В: Дорогий",
            price=200000,
            area=180,
            has_gas=True,
            has_water=True,
            has_sewer=True,
            has_electricity=True,
            has_heating=True,
            has_bathroom=True,
            condition="excellent",
            location_rating=9
        )
    ]
    
    evaluator = HomeEvaluator()
    results = evaluator.compare_houses(houses)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['house_name']}: {result['final_score']:.2f} балів")
        print(f"   Ціна: ${result['house']['price']:,.0f}, Площа: {result['house']['area']}м²")
    print()


def example_custom_weights():
    """Використання власних вагових коефіцієнтів"""
    print("=" * 80)
    print("ПРИКЛАД 3: Власні вагові коефіцієнти")
    print("=" * 80)
    
    # Створюємо будинок
    house = House(
        name="Тестовий будинок",
        price=100000,
        area=100,
        has_gas=True,
        has_water=True,
        has_sewer=True,
        has_electricity=True,
        has_heating=True,
        has_bathroom=True,
        condition="good",
        location_rating=7,
        year_built=2005
    )
    
    # Стандартні ваги
    evaluator_standard = HomeEvaluator()
    result_standard = evaluator_standard.evaluate_house(house)
    
    # Власні ваги (припустимо, ціна дуже важлива)
    custom_weights = EvaluationWeights(
        price_weight=30.0,  # Збільшуємо вагу ціни
        area_weight=5.0,
        gas_weight=5.0,
        water_weight=5.0,
        sewer_weight=5.0,
        electricity_weight=5.0,
        heating_weight=10.0,
        bathroom_weight=10.0,
        kitchen_weight=5.0,
        condition_weight=10.0,
        location_weight=10.0,
        garden_weight=2.0,
        garage_weight=2.0,
        year_weight=5.0,
        floors_weight=2.0,
        distance_weight=5.0
    )
    
    evaluator_custom = HomeEvaluator(custom_weights)
    result_custom = evaluator_custom.evaluate_house(house)
    
    print(f"Стандартні ваги: {result_standard['final_score']:.2f} балів")
    print(f"Власні ваги (ціна важливіша): {result_custom['final_score']:.2f} балів")
    print()


def example_load_from_json():
    """Завантаження будинків з JSON файлу"""
    print("=" * 80)
    print("ПРИКЛАД 4: Завантаження з JSON файлу")
    print("=" * 80)
    
    try:
        with open('data/houses.json', 'r', encoding='utf-8') as f:
            houses_data = json.load(f)
        
        houses = [House.from_dict(data) for data in houses_data]
        
        evaluator = HomeEvaluator()
        results = evaluator.compare_houses(houses, sort_by="final_score")
        
        print("Топ 5 будинків за фінальним балом:")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result['house_name']}: {result['final_score']:.2f} балів")
            print(f"   Ціна: ${result['house']['price']:,.0f}, Площа: {result['house']['area']}м²")
        print()
        
    except FileNotFoundError:
        print("Файл houses.json не знайдено. Створіть його з прикладами будинків.")
        print()


def example_detailed_analysis():
    """Детальний аналіз будинку"""
    print("=" * 80)
    print("ПРИКЛАД 5: Детальний аналіз")
    print("=" * 80)
    
    house = House(
        name="Детальний аналіз",
        price=120000,
        area=140,
        has_gas=True,
        has_water=True,
        has_sewer=True,
        has_electricity=True,
        has_heating=True,
        has_bathroom=True,
        has_kitchen=True,
        condition="excellent",
        location_rating=8,
        year_built=2015,
        floors=2,
        has_garden=True,
        has_garage=True,
        distance_to_city=10
    )
    
    evaluator = HomeEvaluator()
    result = evaluator.evaluate_house(house)
    
    print(f"Будинок: {result['house_name']}")
    print(f"Фінальний бал: {result['final_score']:.2f}/100")
    print()
    print("Детальний розрахунок:")
    print("-" * 50)
    
    for factor, data in result['scores'].items():
        print(f"{factor:20s}: {data['score']:.3f} x {data['weighted']:.2f} = {data['weighted']:.2f}")
    
    print("-" * 50)
    print(f"{'Сума вагових балів':20s}: {result['total_weighted']:.2f}")
    print(f"{'Сумарна вага':20s}: {result['total_weight']:.2f}")
    print()


def example_save_load_weights():
    """Збереження та завантаження вагових коефіцієнтів"""
    print("=" * 80)
    print("ПРИКЛАД 6: Збереження та завантаження ваг")
    print("=" * 80)
    
    # Створюємо власні ваги
    custom_weights = EvaluationWeights(
        price_weight=20.0,
        area_weight=15.0,
        condition_weight=15.0,
        location_weight=15.0
    )
    
    evaluator = HomeEvaluator(custom_weights)
    
    # Зберігаємо ваги у файл
    evaluator.save_weights('custom_weights.json')
    print("Вага збережені у файл custom_weights.json")
    
    # Завантажуємо ваги з файлу
    evaluator.load_weights('custom_weights.json')
    print("Вага завантажені з файлу")
    
    # Тестуємо
    house = House(
        name="Тест",
        price=100000,
        area=100,
        condition="good",
        location_rating=7
    )
    
    result = evaluator.evaluate_house(house)
    print(f"Бал з завантаженими вагами: {result['final_score']:.2f}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ПРИКЛАДИ ВИКОРИСТАННЯ HOME EVALUATOR")
    print("=" * 80 + "\n")
    
    example_basic_usage()
    example_compare_houses()
    example_custom_weights()
    example_load_from_json()
    example_detailed_analysis()
    
    try:
        example_save_load_weights()
    except Exception as e:
        print(f"Помилка в прикладі 6: {e}")
