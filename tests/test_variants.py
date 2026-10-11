"""Тридцять відкритих наборів даних з карток: запускайте лише свій, наприклад pytest -k v13."""
import pytest
from cases import SETS, check


def _params():
    return [pytest.param(task, args, expected, id=f"v{index + 1:02d}")
            for index, (task, label, args, expected) in enumerate(SETS)]


@pytest.mark.parametrize("task,args,expected", _params())
def test_набір_з_картки(task, args, expected):
    check(task, args, expected)
