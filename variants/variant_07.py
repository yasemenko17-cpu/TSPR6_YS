"""Задача 7. Критичний шлях і резерви часу.

Правила: student.md, розділ «Опис задач», задача 7.
Відкриті тести: pytest -k v19 (набір A), v20 (набір B), v21 (набір C).
"""


def critical_path(tasks: list) -> dict:
    """Рахує ранні й пізні терміни, резерв часу кожної задачі та критичний шлях."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(critical_path([{"id": "A", "days": 3, "depends_on": []}]))
