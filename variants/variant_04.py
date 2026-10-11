"""Задача 4. Імовірнісний прогноз кількості спринтів (Монте-Карло).

Правила: student.md, розділ «Опис задач», задача 4.
Відкриті тести: pytest -k v10 (набір A), v11 (набір B), v12 (набір C).
"""


def forecast_sprints(remaining: int, history: list, runs: int, seed: int) -> dict:
    """Багаторазово моделює завершення роботи, беручи швидкість спринту з історії власним детермінованим генератором."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(forecast_sprints(12, [5, 10], 3, 1))
