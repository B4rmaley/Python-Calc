"""Калькулятор: разбор и вычисление выражений
Пайплайн:
        tokenize(expr) -> list[str]
        validate(tokens) -> None (бросает ToolkitError)
        calculate(expr) -> float   (recursive descent)
Поддерживаются: + - * /, унарные + -, скобки, числа с плавающей точкой
Без eval/exec
"""
from src.errors import DivisionByZeroError, EmptyExpressionError, InvalidCharacterError, MissingOperandError


def tokenize(expr: str) -> list[str]:
    """Разбить строку на токены: числа, операторы и скобки.
    Пробелы игнорируются. Числа собираются целиком (например, '2.5').
        Args:
            expr: строка с арифметическим выражением.

        Returns:
            Список токенов (строк).

        Raises:
            InvalidCharacterError: если встретился недопустимый символ (например, буква).
    """
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        # пробелы  пропускаются.
        if ch.isspace():
            i += 1
        # оператор/скобка добавляеются как отдельный токен
        elif ch in "+-*/()":
            tokens.append(ch)
            i += 1
        # цифры/точка являются началом числа
        elif ch.isdigit() or ch == '.':
            start = i
            # смещение позиции до первого символа, не являющегося цифрой/точкой
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            # извлечение числа целиком
            tokens.append(expr[start:i])
        # Любой другой символ является ошибкой
        else:
            raise InvalidCharacterError(f"Недопустимый символ: {ch}")
    return tokens


def validate(tokens: list[str]) -> None:
    """Проверка на логичность последовательности токенов
    ошибка: пустое выражение, два оператора подряд (кроме унарного +/-), два числа подряд, выражение, заканчивающееся оператором
    Args:
        tokens: список токенов из tokenize()
    Raises:
        EmptyExpressionError: если список токенов пуст
        MissingOperandError: если нарушен порядок операторов и операндов
    """
    if not tokens:
        raise EmptyExpressionError("Пустое выражение")

    # Флаг: ожидание числа в текущей позиции
    expect_operand = True
    for t in tokens:
        if t in "+-*/":
            # допускаются унарные + или - в ожидании числа
            if expect_operand and t in "+-":
                continue
            # бинарный оператор в позиции ожидании числа - ошибка
            if expect_operand:
                raise MissingOperandError(f"Пропущен операнд перед {t}")
            # после оператора ожидается число
            expect_operand = True
        elif t == "(":
            # после открывающейся скобки ожидается число; после закрывающейся скобки не ожидается
            expect_operand = True
        elif t == ")":
            expect_operand = False
        else:
            # если число не ожидается в данной позиции - ошибка
            if not expect_operand:
                raise MissingOperandError("Два числа подряд")
            expect_operand = False

    # если при завершении цикла выражение заканчивается оператором - ошибка
    if expect_operand:
        raise MissingOperandError("Выражение не может заканчиваться оператором")


def calculate(expr: str) -> float:
    """Вычисление выражения
    Используется рекурсивный спуск: parse_expr -> parse_term -> parse_factor
    Учитывается приоритет операций, унарные +/-, скобки
    Args:
        expr: строка с выражением
    Returns:
        Результат вычисления как float
    Raises:
        ToolkitError: любая доменная ошибка
    """
    tokens = tokenize(expr)       # 1. строка разбивается на токены
    validate(tokens)              # 2. проверка корректности логики

    pos = 0  # текущая позиция в списке токенов

    def current():
        """Возвращается текущий токен или None, если токены кончились"""
        return tokens[pos] if pos < len(tokens) else None

    def parse_factor():
        """Обработка числа/скобки/унарного + или - (высший приоритет)"""
        nonlocal pos
        tok = current()
        if tok is None:
            raise MissingOperandError("Неожиданный конец выражения")

        # унарный плюс/минус
        if tok in ("+", "-"):
            pos += 1
            val = parse_factor()  # рекурсивный вызов для следующего фактора
            return val if tok == "+" else -val

        # Скобки
        if tok == "(":
            pos += 1
            val = parse_expr()  # внутри скобок разбор идёт с низкого приоритета
            if current() != ")":
                raise MissingOperandError("Ожидалась закрывающая скобка")
            pos += 1
            return val

        # Число
        try:
            val = float(tok)
            pos += 1
            return val
        except ValueError:
            raise MissingOperandError(f"Ожидалось число, получено {tok}")

    def parse_term():
        """Обработатка умножения и деления (средний приоритет)."""
        nonlocal pos
        val = parse_factor()  # сначала обрабатывается число/скобка
        while current() in ("*", "/"):
            op = tokens[pos]
            pos += 1
            right = parse_factor()
            if op == "*":
                val *= right
            else:
                # ошибка деления на ноль.
                if right == 0:
                    raise DivisionByZeroError("Деление на ноль")
                val /= right
        return val

    def parse_expr():
        """Обработка сложения/вычитания (низкий приоритет)."""
        nonlocal pos
        val = parse_term()  # сначала вычисляется умножение/деление
        while current() in ("+", "-"):
            op = tokens[pos]
            pos += 1
            right = parse_term()
            val = val + right if op == "+" else val - right
        return val

    return float(parse_expr())