#!/usr/bin/env python3
"""
Home Evaluator - Система оцінки будинків за різними факторами

Ця програма допомагає оцінити будинок за різними критеріями:
- Ціна
- Площа
- Наявність комунікацій (газ, вода, електрика)
- Стан будинку (ремонт)
- Розташування
- та інші фактори

Кожному фактору призначений ваговий коефіцієнт, і фінальний бал
рахується від 0 до 100.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class House:
    """Клас для представлення будинку"""
    name: str
    price: float  # Ціна в доларах
    area: float  # Площа в м²
    has_gas: bool = False
    has_water: bool = False
    has_sewer: bool = False
    has_electricity: bool = False
    has_heating: bool = False
    has_bathroom: bool = False
    has_kitchen: bool = False
    condition: str = "old"  # old, average, good, excellent
    location_rating: int = 5  # Оцінка розташування від 1 до 10
    year_built: Optional[int] = None
    floors: int = 1
    has_garden: bool = False
    has_garage: bool = False
    distance_to_city: Optional[float] = None  # у кілометрах
    
    def to_dict(self) -> Dict:
        """Конвертація в словник"""
        return {
            "name": self.name,
            "price": self.price,
            "area": self.area,
            "has_gas": self.has_gas,
            "has_water": self.has_water,
            "has_sewer": self.has_sewer,
            "has_electricity": self.has_electricity,
            "has_heating": self.has_heating,
            "has_bathroom": self.has_bathroom,
            "has_kitchen": self.has_kitchen,
            "condition": self.condition,
            "location_rating": self.location_rating,
            "year_built": self.year_built,
            "floors": self.floors,
            "has_garden": self.has_garden,
            "has_garage": self.has_garage,
            "distance_to_city": self.distance_to_city
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "House":
        """Створення з словника"""
        return cls(**data)


@dataclass
class EvaluationWeights:
    """Вагові коефіцієнти для оцінки будинку"""
    
    # Вага ціни (нижча ціна - краще)
    price_weight: float = 15.0
    
    # Вага площі (більша площа - краще)
    area_weight: float = 10.0
    
    # Вага комунікацій
    gas_weight: float = 8.0
    water_weight: float = 8.0
    sewer_weight: float = 7.0
    electricity_weight: float = 5.0
    heating_weight: float = 10.0
    bathroom_weight: float = 10.0
    kitchen_weight: float = 5.0
    
    # Вага стану будинку
    condition_weight: float = 10.0
    
    # Вага розташування
    location_weight: float = 10.0
    
    # Вага інших факторів
    garden_weight: float = 2.0
    garage_weight: float = 3.0
    year_weight: float = 5.0
    floors_weight: float = 2.0
    distance_weight: float = 5.0
    
    def to_dict(self) -> Dict:
        """Конвертація в словник"""
        return {
            "price_weight": self.price_weight,
            "area_weight": self.area_weight,
            "gas_weight": self.gas_weight,
            "water_weight": self.water_weight,
            "sewer_weight": self.sewer_weight,
            "electricity_weight": self.electricity_weight,
            "heating_weight": self.heating_weight,
            "bathroom_weight": self.bathroom_weight,
            "kitchen_weight": self.kitchen_weight,
            "condition_weight": self.condition_weight,
            "location_weight": self.location_weight,
            "garden_weight": self.garden_weight,
            "garage_weight": self.garage_weight,
            "year_weight": self.year_weight,
            "floors_weight": self.floors_weight,
            "distance_weight": self.distance_weight
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EvaluationWeights":
        """Створення з словника"""
        return cls(**data)
    
    def total_weight(self) -> float:
        """Сумарна вага всіх факторів"""
        return sum(vars(self).values())


class HomeEvaluator:
    """Основний клас для оцінки будинків"""
    
    # Стандартні значення для нормалізації
    REFERENCE_PRICE = 100000  # Базова ціна для порівняння
    REFERENCE_AREA = 100  # Базова площа для порівняння
    REFERENCE_YEAR = 2000  # Базовий рік побудови
    MAX_DISTANCE = 50  # Максимальна відстань до міста для нормалізації
    
    CONDITION_SCORES = {
        "excellent": 1.0,
        "good": 0.8,
        "average": 0.5,
        "old": 0.2
    }
    
    def __init__(self, weights: Optional[EvaluationWeights] = None):
        """Ініціалізація з ваговими коефіцієнтами"""
        self.weights = weights or EvaluationWeights()
    
    def normalize_price(self, price: float) -> float:
        """Нормалізація ціни (нижча ціна - краще)"""
        # Чим нижча ціна, тим вищий бал
        if price <= 0:
            return 0.0
        return min(1.0, self.REFERENCE_PRICE / price)
    
    def normalize_area(self, area: float) -> float:
        """Нормалізація площі (більша площа - краще)"""
        if area <= 0:
            return 0.0
        return min(1.0, area / self.REFERENCE_AREA)
    
    def normalize_year(self, year: Optional[int]) -> float:
        """Нормалізація року побудови (новіший - краще)"""
        if year is None:
            return 0.5
        if year >= self.REFERENCE_YEAR:
            return 1.0
        return max(0.0, min(1.0, (year - 1900) / 100))
    
    def normalize_distance(self, distance: Optional[float]) -> float:
        """Нормалізація відстані до міста (ближче - краще)"""
        if distance is None:
            return 0.5
        if distance <= 0:
            return 1.0
        return max(0.0, min(1.0, 1 - (distance / self.MAX_DISTANCE)))
    
    def normalize_floors(self, floors: int) -> float:
        """Нормалізація кількості поверхів"""
        if floors <= 0:
            return 0.0
        return min(1.0, floors / 3)  # 3 поверхи - максимум
    
    def evaluate_condition(self, condition: str) -> float:
        """Оцінка стану будинку"""
        return self.CONDITION_SCORES.get(condition.lower(), 0.2)
    
    def evaluate_house(self, house: House, custom_params: Optional[List[Dict]] = None, custom_weights: Optional[Dict] = None) -> Dict:
        """
        Оцінка будинку за всіма факторами
        
        Args:
            house: Будинок для оцінки
            custom_params: Список кастомних параметрів (опціонально)
            custom_weights: Словник з кастомними вагами (опціонально)
        
        Returns:
            Dict з детальним розрахунком і фінальним балом
        """
        scores = {}
        
        # Оцінка ціни
        price_score = self.normalize_price(house.price)
        scores["price"] = {
            "value": house.price,
            "score": price_score,
            "weighted": price_score * self.weights.price_weight
        }
        
        # Оцінка площі
        area_score = self.normalize_area(house.area)
        scores["area"] = {
            "value": house.area,
            "score": area_score,
            "weighted": area_score * self.weights.area_weight
        }
        
        # Оцінка комунікацій
        scores["has_gas"] = {
            "value": house.has_gas,
            "score": 1.0 if house.has_gas else 0.0,
            "weighted": (1.0 if house.has_gas else 0.0) * self.weights.gas_weight
        }
        
        scores["has_water"] = {
            "value": house.has_water,
            "score": 1.0 if house.has_water else 0.0,
            "weighted": (1.0 if house.has_water else 0.0) * self.weights.water_weight
        }
        
        scores["has_sewer"] = {
            "value": house.has_sewer,
            "score": 1.0 if house.has_sewer else 0.0,
            "weighted": (1.0 if house.has_sewer else 0.0) * self.weights.sewer_weight
        }
        
        scores["has_electricity"] = {
            "value": house.has_electricity,
            "score": 1.0 if house.has_electricity else 0.0,
            "weighted": (1.0 if house.has_electricity else 0.0) * self.weights.electricity_weight
        }
        
        scores["has_heating"] = {
            "value": house.has_heating,
            "score": 1.0 if house.has_heating else 0.0,
            "weighted": (1.0 if house.has_heating else 0.0) * self.weights.heating_weight
        }
        
        scores["has_bathroom"] = {
            "value": house.has_bathroom,
            "score": 1.0 if house.has_bathroom else 0.0,
            "weighted": (1.0 if house.has_bathroom else 0.0) * self.weights.bathroom_weight
        }
        
        scores["has_kitchen"] = {
            "value": house.has_kitchen,
            "score": 1.0 if house.has_kitchen else 0.0,
            "weighted": (1.0 if house.has_kitchen else 0.0) * self.weights.kitchen_weight
        }
        
        # Оцінка стану
        condition_score = self.evaluate_condition(house.condition)
        scores["condition"] = {
            "value": house.condition,
            "score": condition_score,
            "weighted": condition_score * self.weights.condition_weight
        }
        
        # Оцінка розташування
        location_score = house.location_rating / 10.0
        scores["location_rating"] = {
            "value": house.location_rating,
            "score": location_score,
            "weighted": location_score * self.weights.location_weight
        }
        
        # Оцінка інших факторів
        scores["has_garden"] = {
            "value": house.has_garden,
            "score": 1.0 if house.has_garden else 0.0,
            "weighted": (1.0 if house.has_garden else 0.0) * self.weights.garden_weight
        }
        
        scores["has_garage"] = {
            "value": house.has_garage,
            "score": 1.0 if house.has_garage else 0.0,
            "weighted": (1.0 if house.has_garage else 0.0) * self.weights.garage_weight
        }
        
        year_score = self.normalize_year(house.year_built)
        scores["year_built"] = {
            "value": house.year_built,
            "score": year_score,
            "weighted": year_score * self.weights.year_weight
        }
        
        floors_score = self.normalize_floors(house.floors)
        scores["floors"] = {
            "value": house.floors,
            "score": floors_score,
            "weighted": floors_score * self.weights.floors_weight
        }
        
        distance_score = self.normalize_distance(house.distance_to_city)
        scores["distance_to_city"] = {
            "value": house.distance_to_city,
            "score": distance_score,
            "weighted": distance_score * self.weights.distance_weight
        }
        
        # Додаємо кастомні параметри
        if custom_params:
            custom_scores = self._evaluate_custom_params(house, custom_params, custom_weights or {})
            scores.update(custom_scores)
            
            # Оновлюємо ваги з кастомними
            if custom_weights:
                for param_name, param_data in custom_weights.items():
                    if param_name.endswith('_weight'):
                        # Додаємо вагу до загальної суми
                        pass  # Ваги вже враховані у custom_scores
        
        # Сумарний ваговий бал
        total_weighted = sum(s["weighted"] for s in scores.values())
        total_weight = self.weights.total_weight()
        
        # Додаємо ваги кастомних параметрів
        if custom_weights:
            for param_name, weight_value in custom_weights.items():
                if param_name.endswith('_weight'):
                    total_weight += weight_value
        
        # Фінальний бал від 0 до 100
        final_score = (total_weighted / total_weight) * 100 if total_weight > 0 else 0
        
        return {
            "house_name": house.name,
            "scores": scores,
            "total_weighted": total_weighted,
            "total_weight": total_weight,
            "final_score": round(final_score, 2)
        }
    
    def _evaluate_custom_params(self, house: House, custom_params: List[Dict], custom_weights: Dict) -> Dict:
        """
        Оцінка кастомних параметрів
        
        Args:
            house: Будинок
            custom_params: Список кастомних параметрів
            custom_weights: Словник з вагами для кастомних параметрів
        
        Returns:
            Словник з оцінками кастомних параметрів
        """
        custom_scores = {}
        
        for param in custom_params:
            param_name = param.get('name', '')
            param_type = param.get('type', 'bool')
            param_weight = custom_weights.get(f'{param_name}_weight', 5.0)
            
            # Отримуємо значення параметра з будинку
            house_dict = house.to_dict()
            param_value = house_dict.get(param_name)
            
            # Якщо параметр не вказано, використовуємо значення за замовчуванням
            if param_value is None:
                # Для булевих параметрів - False
                if param_type == 'bool':
                    param_value = False
                # Для числових - 0
                elif param_type == 'float':
                    param_value = 0
                # Для вибору - перший варіант
                elif param_type == 'select':
                    options = param.get('options', ['low', 'medium', 'high'])
                    param_value = options[0] if options else None
                else:
                    param_value = None
            
            # Рахуємо бал залежно від типу
            if param_type == 'bool':
                # Булевий параметр: 1.0 якщо True, 0.0 якщо False
                score = 1.0 if param_value else 0.0
            elif param_type == 'float':
                # Числовий параметр: нормалізуємо до діапазону 0-1
                if param_value is None:
                    score = 0.5  # Середній бал для відсутнього значення
                else:
                    # Для числових параметрів використовуємо нормалізацію
                    # Можна налаштувати індивідуально для кожного параметра
                    score = min(1.0, max(0.0, param_value / 100.0))
            elif param_type == 'select':
                # Параметр вибору: мапуємо опції до балів
                options = param.get('options', ['low', 'medium', 'high'])
                if param_value in options:
                    score = (options.index(param_value) + 1) / len(options)
                else:
                    score = 0.5  # Середній бал для невідомої опції
            else:
                score = 0.5  # Середній бал за замовчуванням
            
            custom_scores[param_name] = {
                "value": param_value,
                "score": score,
                "weighted": score * param_weight
            }
        
        return custom_scores
    
    def evaluate_multiple(self, houses: List[House], custom_params: Optional[List[Dict]] = None, custom_weights: Optional[Dict] = None) -> List[Dict]:
        """Оцінка декількох будинків"""
        return [self.evaluate_house(house, custom_params, custom_weights) for house in houses]
    
    def compare_houses(self, houses: List[House], sort_by: str = "final_score", custom_params: Optional[List[Dict]] = None, custom_weights: Optional[Dict] = None) -> List[Dict]:
        """
        Порівняння декількох будинків з сортуванням
        
        Args:
            houses: Список будинків
            sort_by: Поле для сортування (final_score, price, area, etc.)
            custom_params: Список кастомних параметрів (опціонально)
            custom_weights: Словник з кастомними вагами (опціонально)
        
        Returns:
            Відсортований список з оцінками
        """
        evaluations = self.evaluate_multiple(houses, custom_params, custom_weights)
        
        # Додаємо оригінальні дані будинку
        for eval_result, house in zip(evaluations, houses):
            eval_result["house"] = house.to_dict()
        
        # Сортуємо
        reverse = sort_by != "price"  # Для ціни сортуємо за зростанням
        evaluations.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
        
        return evaluations
    
    def save_weights(self, filepath: str):
        """Збереження ваг у файл"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.weights.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_weights(self, filepath: str):
        """Завантаження ваг з файлу"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.weights = EvaluationWeights.from_dict(data)


def create_sample_houses() -> List[House]:
    """Створення прикладних будинків для тестування"""
    return [
        House(
            name="Будинок 1: Дешевий, але без комунікацій",
            price=50000,
            area=80,
            has_gas=False,
            has_water=True,
            has_sewer=False,
            has_electricity=True,
            has_heating=False,
            has_bathroom=False,
            has_kitchen=True,
            condition="old",
            location_rating=4,
            year_built=1980,
            floors=1,
            has_garden=True,
            has_garage=False,
            distance_to_city=20
        ),
        House(
            name="Будинок 2: Дорогий, але з усіма",
            price=200000,
            area=150,
            has_gas=True,
            has_water=True,
            has_sewer=True,
            has_electricity=True,
            has_heating=True,
            has_bathroom=True,
            has_kitchen=True,
            condition="excellent",
            location_rating=9,
            year_built=2020,
            floors=2,
            has_garden=True,
            has_garage=True,
            distance_to_city=5
        ),
        House(
            name="Будинок 3: Середній варіант",
            price=100000,
            area=120,
            has_gas=True,
            has_water=True,
            has_sewer=True,
            has_electricity=True,
            has_heating=True,
            has_bathroom=True,
            has_kitchen=True,
            condition="good",
            location_rating=7,
            year_built=2005,
            floors=1,
            has_garden=True,
            has_garage=False,
            distance_to_city=10
        ),
        House(
            name="Будинок 4: Старий, але дешевий і близько до міста",
            price=40000,
            area=60,
            has_gas=False,
            has_water=True,
            has_sewer=False,
            has_electricity=True,
            has_heating=False,
            has_bathroom=False,
            has_kitchen=True,
            condition="old",
            location_rating=8,
            year_built=1970,
            floors=1,
            has_garden=False,
            has_garage=False,
            distance_to_city=2
        ),
        House(
            name="Будинок 5: Сучасний за містом",
            price=150000,
            area=180,
            has_gas=True,
            has_water=True,
            has_sewer=True,
            has_electricity=True,
            has_heating=True,
            has_bathroom=True,
            has_kitchen=True,
            condition="excellent",
            location_rating=6,
            year_built=2018,
            floors=2,
            has_garden=True,
            has_garage=True,
            distance_to_city=30
        )
    ]


if __name__ == "__main__":
    # Створення евалюатора
    evaluator = HomeEvaluator()
    
    # Створення прикладних будинків
    houses = create_sample_houses()
    
    # Оцінка будинків
    print("=" * 80)
    print("ОЦІНКА БУДИНКІВ")
    print("=" * 80)
    print()
    
    evaluations = evaluator.compare_houses(houses, sort_by="final_score")
    
    for i, eval_result in enumerate(evaluations, 1):
        print(f"{i}. {eval_result['house_name']}")
        print(f"   Фінальний бал: {eval_result['final_score']:.2f}/100")
        print(f"   Ціна: ${eval_result['house']['price']:,.0f}")
        print(f"   Площа: {eval_result['house']['area']} м²")
        print()
    
    # Детальний розрахунок для першого будинку
    print("=" * 80)
    print("ДЕТАЛЬНИЙ РОЗРАХУНОК для першого будинку")
    print("=" * 80)
    first_eval = evaluations[0]
    for factor, data in first_eval['scores'].items():
        print(f"{factor:20s}: {data['score']:.3f} (вага: {data['weighted']:.2f})")
    print(f"{'Сума вагових балів':20s}: {first_eval['total_weighted']:.2f}")
    print(f"{'Сумарна вага':20s}: {first_eval['total_weight']:.2f}")
    print(f"{'Фінальний бал':20s}: {first_eval['final_score']:.2f}")
