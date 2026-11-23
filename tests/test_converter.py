"""Тесты конвертера"""

import pytest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


def test_mm_to_m():
    """1000 мм = 1 метр."""
    assert convert(1000, "mm", "m") == pytest.approx(1.0)


def test_kg_to_g():
    """1.5 кг = 1500 грамм."""
    assert convert(1.5, "kg", "g") == pytest.approx(1500.0)


def test_c_to_f():
    """0 °C = 32 °F."""
    assert convert(0, "c", "f") == pytest.approx(32.0)


def test_c_to_k():
    """-273.15 °C = 0 K."""
    assert convert(-273.15, "c", "k") == pytest.approx(0.0)


def test_100c_to_f():
    """100 °C = 212 °F."""
    assert convert(100, "c", "f") == pytest.approx(212.0)


def test_m_to_cm():
    """1 м = 100 см."""
    assert convert(1, "m", "cm") == pytest.approx(100.0)


def test_case_insensitive():
    """Регистр не важен"""
    assert convert(1, "KM", "M") == pytest.approx(1000.0)


def test_below_absolute_zero():
    """Температура ниже абсолютного нуля - ошибка"""
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-300, "c", "k")


def test_incompatible_units():
    """Массу в длину перевести нельзя - ошибка"""
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "kg", "m")


def test_unknown_unit():
    """Неизвестная единица - ошибка"""
    with pytest.raises(UnknownUnitError):
        convert(1, "golda", "m")