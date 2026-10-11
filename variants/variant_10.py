"""Задача 10. Порівняння плану з фактом: освоєний обсяг.

Правила: student.md, розділ «Опис задач», задача 10.
Відкриті тести: pytest -k v28 (набір A), v29 (набір B), v30 (набір C).
"""


def plan_vs_fact(scope: int, budget: int, sprints: list) -> dict:
    """Порівнює виконане із запланованим за обсягом і витратами та прогнозує підсумок за поточного темпу."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(plan_vs_fact(100, 1000, [{"planned": 20, "done": 18, "hours": 190}]))
