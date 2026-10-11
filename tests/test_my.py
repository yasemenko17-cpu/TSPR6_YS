import pytest
from conftest import load

solve = load(8).level_plan

def test_level_plan_duplicate_id():
    """Перевірка помилки повторного ID у задачах."""
    tasks = [
        {'id': 'A', 'points': 3, 'depends_on': []},
        {'id': 'A', 'points': 5, 'depends_on': []}
    ]
    with pytest.raises(ValueError, match="Повторний id: A"):
        solve(tasks, [10], [['A']])

def test_level_plan_cycle():
    """Перевірка виявлення циклу залежностей."""
    tasks = [
        {'id': 'X', 'points': 2, 'depends_on': ['Y']},
        {'id': 'Y', 'points': 2, 'depends_on': ['X']}
    ]
    with pytest.raises(ValueError, match="Цикл залежностей"):
        solve(tasks, [10], [['X', 'Y']])

def test_level_plan_task_not_in_plan():
    """Перевірка помилки, якщо задача є в tasks, але відсутня в плані."""
    tasks = [
        {'id': 'A', 'points': 3, 'depends_on': []},
        {'id': 'B', 'points': 4, 'depends_on': []}
    ]
    with pytest.raises(ValueError, match="Задача не в плані: B"):
        solve(tasks, [10], [['A']])