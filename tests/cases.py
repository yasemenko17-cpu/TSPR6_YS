"""Тридцять наборів даних з карток: по три для кожної з десяти задач.

Кожен запис SETS: (номер задачі, мітка набору, аргументи виклику, очікуваний результат).
Очікувані значення розраховано вручну з умови картки (розрахунки: teacher.md); крайні випадки лежать у закритих тестах.
"""
import copy
import signal

import pytest
from conftest import load

FUNCTIONS = {
    1: "consolidate_votes", 2: "calibrate_points", 3: "velocity_band", 4: "forecast_sprints", 5: "sprint_calendar",
    6: "pert_estimate", 7: "critical_path", 8: "level_plan", 9: "build_roadmap", 10: "plan_vs_fact",
}


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


class Timeout(Exception):
    """Розв'язок виконується надто довго (ймовірно, нескінченний цикл)."""


def _alarm(signum, frame):
    raise Timeout("перевищено 10 секунд: перевірте умови завершення циклів")


def check(task, args, expected):
    """Викликає функцію задачі, порівнює результат або текст помилки й стежить, щоб вхідні дані не змінилися."""
    function = getattr(load(task), FUNCTIONS[task])
    before = copy.deepcopy(args)
    guarded = hasattr(signal, "SIGALRM")
    if guarded:
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(10)
    try:
        if isinstance(expected, ValueError):
            with pytest.raises(ValueError) as info:
                function(*args)
            assert str(info.value) == str(expected)
        else:
            assert norm(function(*args)) == norm(expected)
    finally:
        if guarded:
            signal.alarm(0)
    assert args == before, "функція не повинна змінювати вхідні дані"


SETS = [
    # задача 1, набір A: Команда інтернет-магазину
    (1, "A", ({'Кошик': {'Оля': 3, 'Іра': 5, 'Петро': 3},
      'Купони': {'Оля': 2, 'Іра': 8, 'Петро': None},
      'Відгуки': {'Оля': 1, 'Іра': 5, 'Петро': 13}},),
     {'estimates': {'Кошик': 3, 'Купони': 2, 'Відгуки': 5},
      'total': 10,
      'spread': {'Кошик': 1, 'Купони': 3, 'Відгуки': 5},
      'discuss': ['Відгуки', 'Купони'],
      'bias': {'Оля': -1.0, 'Іра': 1.33, 'Петро': 1.0}}),
    # задача 1, набір B: Чотири оцінювачі й утримання
    (1, "B", ({'Вхід': {'Марко': 5, 'Софія': 13, 'Дана': 8, 'Ілля': 8},
      'Профіль': {'Марко': 3, 'Софія': 3, 'Дана': None, 'Ілля': 3},
      'Чат': {'Марко': 2, 'Софія': 8, 'Дана': 21, 'Ілля': 5},
      'Пошта': {'Марко': 8, 'Софія': None, 'Дана': 2, 'Ілля': 13}},),
     {'estimates': {'Вхід': 8, 'Профіль': 3, 'Чат': 5, 'Пошта': 8},
      'total': 24,
      'spread': {'Вхід': 2, 'Профіль': 0, 'Чат': 5, 'Пошта': 4},
      'discuss': ['Чат', 'Пошта', 'Вхід'],
      'bias': {'Марко': -0.75, 'Софія': 0.67, 'Дана': 0.0, 'Ілля': 0.25}}),
    # задача 1, набір C: Учасник, який утримався в усіх
    (1, "C", ({'Реліз': {'Анна': 3, 'Борис': 3, 'Віка': 5, 'Гліб': None},
      'Інфра': {'Анна': 13, 'Борис': 8, 'Віка': 13, 'Гліб': None},
      'Звіти': {'Анна': 2, 'Борис': 3, 'Віка': 2, 'Гліб': None}},),
     {'estimates': {'Реліз': 3, 'Інфра': 13, 'Звіти': 2},
      'total': 18,
      'spread': {'Реліз': 1, 'Інфра': 1, 'Звіти': 1},
      'discuss': [],
      'bias': {'Анна': 0.0, 'Борис': 0.0, 'Віка': 0.33}}),
    # задача 2, набір A: Еталони дають рівно 4 години на очко
    (2, "A", ([{'id': 'R1', 'points': 3, 'hours': 12}, {'id': 'R2', 'points': 5, 'hours': 20}],
     [{'id': 'N1', 'hours': 8}, {'id': 'N2', 'hours': 30}, {'id': 'N3', 'hours': 50}]),
     {'rate': 4.0, 'points': {'N1': 2, 'N2': 8, 'N3': 13}, 'total': 23, 'outliers': []}),
    # задача 2, набір B: Еталони з розбіжністю
    (2, "B", ([{'id': 'R1', 'points': 2, 'hours': 6},
      {'id': 'R2', 'points': 8, 'hours': 24},
      {'id': 'R3', 'points': 5, 'hours': 30}],
     [{'id': 'N1', 'hours': 9}, {'id': 'N2', 'hours': 21}]),
     {'rate': 4.0, 'points': {'N1': 2, 'N2': 5}, 'total': 7, 'outliers': ['R2', 'R3']}),
    # задача 2, набір C: Дробова ставка й межа шкали
    (2, "C", ([{'id': 'E1', 'points': 1, 'hours': 3},
      {'id': 'E2', 'points': 3, 'hours': 11},
      {'id': 'E3', 'points': 8, 'hours': 26}],
     [{'id': 'N1', 'hours': 5},
      {'id': 'N2', 'hours': 14},
      {'id': 'N3', 'hours': 40},
      {'id': 'N4', 'hours': 100}]),
     {'rate': 3.33, 'points': {'N1': 2, 'N2': 5, 'N3': 13, 'N4': 21}, 'total': 41, 'outliers': []}),
    # задача 3, набір A: Стабільна команда
    (3, "A", ([18, 22, 20, 19, 21], 5),
     {'window': 5,
      'mean': 20.0,
      'stdev': 1.58,
      'low': 18.49,
      'high': 21.51,
      'safe': 18,
      'cv': 0.08,
      'predictable': True}),
    # задача 3, набір B: Нестабільна команда
    (3, "B", ([10, 30, 12, 28], 4),
     {'window': 4,
      'mean': 20.0,
      'stdev': 10.46,
      'low': 7.7,
      'high': 32.3,
      'safe': 7,
      'cv': 0.52,
      'predictable': False}),
    # задача 3, набір C: Вікно коротше за історію
    (3, "C", ([5, 40, 20, 22, 21, 19], 4),
     {'window': 4,
      'mean': 20.5,
      'stdev': 1.29,
      'low': 18.98,
      'high': 22.02,
      'safe': 18,
      'cv': 0.06,
      'predictable': True}),
    # задача 4, набір A: Три прогони
    (4, "A", (12, [5, 10], 3, 1),
     {'p50': 3, 'p85': 3, 'p95': 3, 'min': 2, 'max': 3, 'mean': 2.67, 'histogram': {2: 1, 3: 2}}),
    # задача 4, набір B: П'ятдесят прогонів
    (4, "B", (40, [8, 10, 12], 50, 42),
     {'p50': 4, 'p85': 5, 'p95': 5, 'min': 4, 'max': 5, 'mean': 4.36, 'histogram': {4: 32, 5: 18}}),
    # задача 4, набір C: Спринт із нульовою швидкістю
    (4, "C", (30, [0, 6, 9], 100, 2024),
     {'p50': 6,
      'p85': 9,
      'p95': 10,
      'min': 4,
      'max': 18,
      'mean': 6.82,
      'histogram': {4: 10, 5: 15, 6: 27, 7: 18, 8: 13, 9: 8, 10: 5, 11: 1, 12: 2, 18: 1}}),
    # задача 5, набір A: Три спринти без свят
    (5, "A", ('2026-11-02', 10, 3, []),
     {'sprints': [{'n': 1, 'start': '2026-11-02', 'end': '2026-11-13'},
                  {'n': 2, 'start': '2026-11-16', 'end': '2026-11-27'},
                  {'n': 3, 'start': '2026-11-30', 'end': '2026-12-11'}],
      'release': '2026-12-11',
      'calendar_days': 40}),
    # задача 5, набір B: Старт у суботу й свята серед тижня
    (5, "B", ('2026-11-07', 5, 3, ['2026-11-09', '2026-11-11']),
     {'sprints': [{'n': 1, 'start': '2026-11-10', 'end': '2026-11-17'},
                  {'n': 2, 'start': '2026-11-18', 'end': '2026-11-24'},
                  {'n': 3, 'start': '2026-11-25', 'end': '2026-12-01'}],
      'release': '2026-12-01',
      'calendar_days': 22}),
    # задача 5, набір C: Перехід через новорічні свята
    (5, "C", ('2026-12-14', 10, 2, ['2026-12-25', '2027-01-01', '2027-01-07']),
     {'sprints': [{'n': 1, 'start': '2026-12-14', 'end': '2026-12-28'},
                  {'n': 2, 'start': '2026-12-29', 'end': '2027-01-13'}],
      'release': '2027-01-13',
      'calendar_days': 31}),
    # задача 6, набір A: Дві задачі та строк
    (6, "A", ([{'id': 'Дизайн', 'o': 2, 'm': 4, 'p': 12}, {'id': 'Серверна частина', 'o': 3, 'm': 6, 'p': 9}],
     14),
     {'tasks': {'Дизайн': {'e': 5.0, 'var': 2.78}, 'Серверна частина': {'e': 6.0, 'var': 1.0}},
      'expected': 11.0,
      'variance': 3.78,
      'sigma': 1.94,
      'range95': [7.11, 14.89],
      'chance': 0.939}),
    # задача 6, набір B: Чотири задачі без строку
    (6, "B", ([{'id': 'Аналіз', 'o': 1, 'm': 2, 'p': 9},
      {'id': 'Розробка', 'o': 5, 'm': 8, 'p': 17},
      {'id': 'Тести', 'o': 2, 'm': 3, 'p': 4},
      {'id': 'Випуск', 'o': 1, 'm': 1, 'p': 1}],
     None),
     {'tasks': {'Аналіз': {'e': 3.0, 'var': 1.78},
                'Розробка': {'e': 9.0, 'var': 4.0},
                'Тести': {'e': 3.0, 'var': 0.11},
                'Випуск': {'e': 1.0, 'var': 0.0}},
      'expected': 16.0,
      'variance': 5.89,
      'sigma': 2.43,
      'range95': [11.15, 20.85],
      'chance': None}),
    # задача 6, набір C: Строк менший за очікуване
    (6, "C", ([{'id': 'Міграція', 'o': 4, 'm': 10, 'p': 22}, {'id': 'Перевірка', 'o': 2, 'm': 5, 'p': 8}], 12),
     {'tasks': {'Міграція': {'e': 11.0, 'var': 9.0}, 'Перевірка': {'e': 5.0, 'var': 1.0}},
      'expected': 16.0,
      'variance': 10.0,
      'sigma': 3.16,
      'range95': [9.68, 22.32],
      'chance': 0.103}),
    # задача 7, набір A: Ромб залежностей
    (7, "A", ([{'id': 'A', 'days': 3, 'depends_on': []},
      {'id': 'B', 'days': 4, 'depends_on': ['A']},
      {'id': 'C', 'days': 2, 'depends_on': ['A']},
      {'id': 'D', 'days': 5, 'depends_on': ['B', 'C']}],),
     {'duration': 12,
      'schedule': {'A': {'es': 0, 'ef': 3, 'ls': 0, 'lf': 3, 'slack': 0},
                   'B': {'es': 3, 'ef': 7, 'ls': 3, 'lf': 7, 'slack': 0},
                   'C': {'es': 3, 'ef': 5, 'ls': 5, 'lf': 7, 'slack': 2},
                   'D': {'es': 7, 'ef': 12, 'ls': 7, 'lf': 12, 'slack': 0}},
      'critical': ['A', 'B', 'D']}),
    # задача 7, набір B: Два однаково довгі шляхи
    (7, "B", ([{'id': 'Дизайн', 'days': 2, 'depends_on': []},
      {'id': 'Фронт', 'days': 6, 'depends_on': ['Дизайн']},
      {'id': 'Бекенд', 'days': 6, 'depends_on': ['Дизайн']},
      {'id': 'Документація', 'days': 3, 'depends_on': ['Дизайн']},
      {'id': 'Інтеграція', 'days': 2, 'depends_on': ['Фронт', 'Бекенд']}],),
     {'duration': 10,
      'schedule': {'Дизайн': {'es': 0, 'ef': 2, 'ls': 0, 'lf': 2, 'slack': 0},
                   'Фронт': {'es': 2, 'ef': 8, 'ls': 2, 'lf': 8, 'slack': 0},
                   'Бекенд': {'es': 2, 'ef': 8, 'ls': 2, 'lf': 8, 'slack': 0},
                   'Документація': {'es': 2, 'ef': 5, 'ls': 7, 'lf': 10, 'slack': 5},
                   'Інтеграція': {'es': 8, 'ef': 10, 'ls': 8, 'lf': 10, 'slack': 0}},
      'critical': ['Дизайн', 'Бекенд', 'Фронт', 'Інтеграція']}),
    # задача 7, набір C: Порядок у списку не збігається з порядком виконання
    (7, "C", ([{'id': 'G', 'days': 1, 'depends_on': ['E', 'F']},
      {'id': 'E', 'days': 4, 'depends_on': ['B']},
      {'id': 'F', 'days': 2, 'depends_on': ['C']},
      {'id': 'B', 'days': 3, 'depends_on': ['A']},
      {'id': 'C', 'days': 5, 'depends_on': ['A']},
      {'id': 'A', 'days': 2, 'depends_on': []},
      {'id': 'H', 'days': 3, 'depends_on': ['A']}],),
     {'duration': 10,
      'schedule': {'G': {'es': 9, 'ef': 10, 'ls': 9, 'lf': 10, 'slack': 0},
                   'E': {'es': 5, 'ef': 9, 'ls': 5, 'lf': 9, 'slack': 0},
                   'F': {'es': 7, 'ef': 9, 'ls': 7, 'lf': 9, 'slack': 0},
                   'B': {'es': 2, 'ef': 5, 'ls': 2, 'lf': 5, 'slack': 0},
                   'C': {'es': 2, 'ef': 7, 'ls': 2, 'lf': 7, 'slack': 0},
                   'A': {'es': 0, 'ef': 2, 'ls': 0, 'lf': 2, 'slack': 0},
                   'H': {'es': 2, 'ef': 5, 'ls': 7, 'lf': 10, 'slack': 5}},
      'critical': ['A', 'B', 'C', 'E', 'F', 'G']}),
    # задача 8, набір A: Перевантажений перший спринт
    (8, "A", ([{'id': 'A', 'points': 5, 'depends_on': []},
      {'id': 'B', 'points': 8, 'depends_on': ['A']},
      {'id': 'C', 'points': 3, 'depends_on': []},
      {'id': 'D', 'points': 5, 'depends_on': []}],
     [10],
     [['A', 'B', 'C'], ['D']]),
     {'sprints': [['A', 'C'], ['B'], ['D']],
      'load': [8, 8, 5],
      'moved': {'B': [1, 2], 'D': [2, 3]},
      'release_sprint': 3}),
    # задача 8, набір B: Спринт зі зменшеною ємністю
    (8, "B", ([{'id': 'T1', 'points': 3, 'depends_on': []},
      {'id': 'T2', 'points': 5, 'depends_on': ['T1']},
      {'id': 'T3', 'points': 2, 'depends_on': ['T2']},
      {'id': 'T4', 'points': 5, 'depends_on': []},
      {'id': 'T5', 'points': 3, 'depends_on': ['T4']}],
     [8, 5, 10],
     [['T1', 'T2', 'T4'], ['T3', 'T5']]),
     {'sprints': [['T1', 'T4'], ['T2'], ['T3', 'T5']],
      'load': [8, 5, 5],
      'moved': {'T2': [1, 2], 'T3': [2, 3], 'T5': [2, 3]},
      'release_sprint': 3}),
    # задача 8, набір C: Менша задача обходить більшу
    (8, "C", ([{'id': 'P', 'points': 6, 'depends_on': []},
      {'id': 'Q', 'points': 5, 'depends_on': []},
      {'id': 'R', 'points': 2, 'depends_on': []},
      {'id': 'S', 'points': 4, 'depends_on': ['P']},
      {'id': 'U', 'points': 3, 'depends_on': ['R']}],
     [10],
     [['P', 'Q', 'R'], ['S'], ['U']]),
     {'sprints': [['P', 'R'], ['Q', 'S'], ['U']],
      'load': [8, 9, 3],
      'moved': {'Q': [1, 2]},
      'release_sprint': 3}),
    # задача 9, набір A: Дві команди
    (9, "A", ([{'id': 'Пошук', 'lane': 'web', 'sprints': 2, 'depends_on': []},
      {'id': 'Кошик', 'lane': 'web', 'sprints': 3, 'depends_on': []},
      {'id': 'Оплата', 'lane': 'api', 'sprints': 2, 'depends_on': ['Пошук']},
      {'id': 'Звіти', 'lane': 'api', 'sprints': 1, 'depends_on': []}],
     2,
     3),
     {'items': {'Пошук': {'start': 1, 'end': 2, 'horizon': 'now', 'waiting_for': None},
                'Кошик': {'start': 3, 'end': 5, 'horizon': 'next', 'waiting_for': 'Пошук'},
                'Оплата': {'start': 3, 'end': 4, 'horizon': 'next', 'waiting_for': 'Пошук'},
                'Звіти': {'start': 5, 'end': 5, 'horizon': 'next', 'waiting_for': 'Оплата'}},
      'release': 5,
      'horizons': {'now': ['Пошук'], 'next': ['Кошик', 'Оплата', 'Звіти'], 'later': []}}),
    # задача 9, набір B: Залежність і послідовність у команді змагаються
    (9, "B", ([{'id': 'Каркас', 'lane': 'core', 'sprints': 2, 'depends_on': []},
      {'id': 'Вхід', 'lane': 'core', 'sprints': 1, 'depends_on': []},
      {'id': 'Профіль', 'lane': 'app', 'sprints': 2, 'depends_on': ['Каркас']},
      {'id': 'Чат', 'lane': 'app', 'sprints': 3, 'depends_on': ['Вхід']}],
     2,
     2),
     {'items': {'Каркас': {'start': 1, 'end': 2, 'horizon': 'now', 'waiting_for': None},
                'Вхід': {'start': 3, 'end': 3, 'horizon': 'next', 'waiting_for': 'Каркас'},
                'Профіль': {'start': 3, 'end': 4, 'horizon': 'next', 'waiting_for': 'Каркас'},
                'Чат': {'start': 5, 'end': 7, 'horizon': 'later', 'waiting_for': 'Профіль'}},
      'release': 7,
      'horizons': {'now': ['Каркас'], 'next': ['Вхід', 'Профіль'], 'later': ['Чат']}}),
    # задача 9, набір C: Три горизонти
    (9, "C", ([{'id': 'Платформа', 'lane': 'A', 'sprints': 3, 'depends_on': []},
      {'id': 'Мобільний клієнт', 'lane': 'B', 'sprints': 4, 'depends_on': ['Платформа']},
      {'id': 'Аналітика', 'lane': 'A', 'sprints': 2, 'depends_on': []},
      {'id': 'Сповіщення', 'lane': 'B', 'sprints': 2, 'depends_on': ['Аналітика']},
      {'id': 'Інтеграції',
       'lane': 'C',
       'sprints': 3,
       'depends_on': ['Мобільний клієнт', 'Сповіщення']}],
     3,
     3),
     {'items': {'Платформа': {'start': 1, 'end': 3, 'horizon': 'now', 'waiting_for': None},
                'Мобільний клієнт': {'start': 4,
                                     'end': 7,
                                     'horizon': 'next',
                                     'waiting_for': 'Платформа'},
                'Аналітика': {'start': 4, 'end': 5, 'horizon': 'next', 'waiting_for': 'Платформа'},
                'Сповіщення': {'start': 8,
                               'end': 9,
                               'horizon': 'later',
                               'waiting_for': 'Мобільний клієнт'},
                'Інтеграції': {'start': 10, 'end': 12, 'horizon': 'later', 'waiting_for': 'Сповіщення'}},
      'release': 12,
      'horizons': {'now': ['Платформа'],
                   'next': ['Аналітика', 'Мобільний клієнт'],
                   'later': ['Сповіщення', 'Інтеграції']}}),
    # задача 10, набір A: Темп за планом
    (10, "A", (100, 1000, [{'planned': 20, 'done': 18, 'hours': 190}, {'planned': 20, 'done': 22, 'hours': 210}]),
     {'variance': [-2, 2],
      'spi': 1.0,
      'cpi': 1.0,
      'eac': 1000.0,
      'overrun': 0.0,
      'forecast_sprints': 5,
      'status': 'за планом'}),
    # задача 10, набір B: Відставання й перевитрата
    (10, "B", (120,
     1800,
     [{'planned': 20, 'done': 15, 'hours': 250},
      {'planned': 20, 'done': 12, 'hours': 260},
      {'planned': 20, 'done': 17, 'hours': 240}]),
     {'variance': [-5, -8, -3],
      'spi': 0.73,
      'cpi': 0.88,
      'eac': 2045.45,
      'overrun': 245.45,
      'forecast_sprints': 9,
      'status': 'відстає'}),
    # задача 10, набір C: Межа відсотка випередження
    (10, "C", (160, 2400, [{'planned': 20, 'done': 22, 'hours': 280}, {'planned': 20, 'done': 20, 'hours': 270}]),
     {'variance': [2, 0],
      'spi': 1.05,
      'cpi': 1.15,
      'eac': 2095.24,
      'overrun': -304.76,
      'forecast_sprints': 8,
      'status': 'випереджає'}),
]
