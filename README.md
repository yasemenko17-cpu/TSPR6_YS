# Стартовий проєкт TSPP-P06

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1` (A, B, C). Реалізуйте функцію задачі у файлі `variants/variant_NN.py` (NN з двома цифрами) за описом у `student.md`.
3. Запускайте відкриті тести лише свого варіанта: `pytest -k v13` (13 — номер варіанта). Права адміністратора не потрібні, окрім `pytest` нічого встановлювати не треба.
4. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py` і `ANSWERS.md`. Файли в `tests/` (крім `test_my.py`) не змінюйте.
5. Розв'язок, що виконується понад 10 секунд, тест зупиняє з помилкою (перевірте умови завершення циклів).
