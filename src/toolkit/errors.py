"""доменные ошибки toolkit.
Все ошибки пользователя идут от ToolkitError
CLI ловит ToolkitError и завершает процесс с кодом 2
"""


class ToolkitError(Exception):
    """Базовая ошибка пользователя.

    От неё наследуются все остальные ошибки приложения,
    чтобы CLI мог поймать любую из них одним блоком except.
    """
    pass


class EmptyExpressionError(ToolkitError):
    """Была передана пустая строка вместо выражения"""
    pass


class InvalidCharacterError(ToolkitError):
    """В выражении встретился недопустимый символ"""
    pass


class MissingOperandError(ToolkitError):
    """Пропущено число или передано 2 операнда подряд"""
    pass


class DivisionByZeroError(ToolkitError):
    """Попытка деления на ноль."""
    pass


class UnknownUnitError(ToolkitError):
    """Была введена единица измерения, которой нет в таблице"""
    pass


class IncompatibleUnitsError(ToolkitError):
    """Попытка перевести несовместимые величины"""
    pass


class BelowAbsoluteZeroError(ToolkitError):
    """Температура ниже абсолютного нуля"""
    pass