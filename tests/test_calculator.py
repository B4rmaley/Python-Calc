"""Тесты калькулятора: позитивные и негативные случаи"""

import pytest

from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MissingOperandError,
)


def test_priority():
    """Умножение выполняется раньше сложения"""
    assert calculate("2+3*4") == 14.0


def test_division():
    """Обычное деление."""
    assert calculate("10 / 4") == 2.5


def test_two_negatives():
    """Унарный минус у обоих чисел: -2 * -3 = 6"""
    assert calculate("-2 * -3") == 6.0


def test_plus_minus():
    """Сложение с отрицательным числом: 1 + -2 = -1"""
    assert calculate("1 + -2") == -1.0


def test_minus_minus():
    """Вычитание отрицательного числа: 2 - -3 = 5"""
    assert calculate("2 - -3") == 5.0


def test_brackets():
    """Скобки меняют порядок вычислений"""
    assert calculate("(2+3)*(4-1)") == 15.0


def test_spaces():
    """Пробелы игнорируются"""
    assert calculate(" 2 * ( 3 + 4 ) ") == 14.0


def test_float():
    """Числа с плавающей точкой"""
    assert calculate("2.5*4") == 10.0


def test_unary_plus():
    """Унарный плюс в начале выражения"""
    assert calculate("+2+3") == 5.0


def test_empty():
    """Пустая строка - ошибка"""
    with pytest.raises(EmptyExpressionError):
        calculate("")


def test_spaces_only():
    """Строка только из пробелов - ошибка"""
    with pytest.raises(EmptyExpressionError):
        calculate("   ")


def test_missing_operand():
    """Пропущен операнд - ошибка"""
    with pytest.raises(MissingOperandError):
        calculate("2*/3")


def test_bad_character():
    """Буква в выражении - ошибка."""
    with pytest.raises(InvalidCharacterError):
        calculate("2+a")


def test_double_operator():
    """Два оператора подряд - ошибка"""
    with pytest.raises(MissingOperandError):
        calculate("2**3")


def test_ends_with_operator():
    """Выражение заканчивается оператором - ошибка"""
    with pytest.raises(MissingOperandError):
        calculate("2+")


def test_starts_with_binary_operator():
    """Выражение начинается с * - ошибка"""
    with pytest.raises(MissingOperandError):
        calculate("*2")


def test_unclosed_bracket():
    """Скобка не закрыта"""
    with pytest.raises(MissingOperandError):
        calculate("(2+3")


def test_extra_closing_bracket():
    """Лишняя закрывающая скобка"""
    with pytest.raises(MissingOperandError):
        calculate("2+3)")


def test_division_by_zero():
    """Деление на ноль - ошибка"""
    with pytest.raises(DivisionByZeroError):
        calculate("1/0")