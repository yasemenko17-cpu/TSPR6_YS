"""Задача 9. Дорожня карта з залежностями та горизонтами Now/Next/Later.

Правила: student.md, розділ «Опис задач», задача 9.
Відкриті тести: pytest -k v25 (набір A), v26 (набір B), v27 (набір C).
"""


def build_roadmap(items: list, now: int, nxt: int) -> dict:
    """Розставляє ініціативи по спринтах з урахуванням залежностей і послідовності в межах команди."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


if __name__ == "__main__":
    print(build_roadmap([{"id": "X", "lane": "web", "sprints": 2, "depends_on": []}], 2, 2))
