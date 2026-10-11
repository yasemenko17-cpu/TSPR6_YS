"""Задача 5. Календар спринтів і дата релізу.

Правила: student.md, розділ «Опис задач», задача 5.
Відкриті тести: pytest -k v13 (набір A), v14 (набір B), v15 (набір C).
"""


def sprint_calendar(start: str, days: int, count: int, holidays: list) -> dict:
    """Розкладає спринти по робочих днях (пн-пт без свят) і повертає календарну дату релізу."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(sprint_calendar("2026-11-02", 10, 2, []))
