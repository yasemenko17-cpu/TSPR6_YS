"""Задача 2. Калібрування Story Points за еталонними задачами.

Правила: student.md, розділ «Опис задач», задача 2.
Відкриті тести: pytest -k v04 (набір A), v05 (набір B), v06 (набір C).
"""


def calibrate_points(reference: list, backlog: list) -> dict:
    """Переводить годинні оцінки нових задач у Story Points за годинами на очко, виміряними на еталонах."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(calibrate_points([{"id": "R1", "points": 3, "hours": 12}], [{"id": "N1", "hours": 8}]))
