"""Задача 8. Вирівнювання плану під ємність спринтів.

Правила: student.md, розділ «Опис задач», задача 8.
Відкриті тести: pytest -k v22 (набір A), v23 (набір B), v24 (набір C).
"""


def level_plan(tasks: list, capacity: list, plan: list) -> dict:
    """Переносить задачі, що не вміщаються в ємність спринту або ще чекають залежностей, у наступні спринти."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(level_plan([{"id": "A", "points": 5, "depends_on": []}], [10], [["A"]]))
