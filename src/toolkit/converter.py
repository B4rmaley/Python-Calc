"""Конвертер величин: длина, масса, температура.
Все единицы длины и массы приводятся к базовой (m, g), затем к целевой.
Температура считается отдельно, так как там не линейный коэффициент.
"""

from src.errors import UnknownUnitError, IncompatibleUnitsError, BelowAbsoluteZeroError

# Единый словарь всех поддерживаемых единиц.
# Формат: "название_единицы": ("группа", коэффициент_к_базовой_единице).
# Для длины базовая единица - метр, для массы - грамм.
# Для температур коэффициент не используется

UNITS = {
    "mm": ("length", 0.001), "cm": ("length", 0.01), "m": ("length", 1.0), "km": ("length", 1000.0),
    "g": ("mass", 1.0), "kg": ("mass", 1000.0),
    "c": ("temp", 1.0), "f": ("temp", 1.0), "k": ("temp", 1.0),
}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """конвертер значений из одной единицы в другую
        args:
            value: числовое значение для перевода
            from_unit: исходная единица (например, "mm", "kg", "c")
            to_unit: целевая единица

        returns:
            Переведённое значение в целевой единице
        
        erros:
            UnknownUnitError: если хотя бы одна из единиц отсутствует в таблице
            IncompatibleUnitsError: если единицы из разных групп
            BelowAbsoluteZeroError: если температура ниже абсолютного нуля (0 K)
    """
    
    
    # названия единиц приводятся к нижнему регистру(верхний и нижний регистр работают одинаково)
    src, dst = from_unit.lower(), to_unit.lower()

    
    # проверк, что обе единиицы существуют в таблице
    if src not in UNITS:
        raise UnknownUnitError(f"Неизвестная единица: {src}")
    if dst not in UNITS:
        raise UnknownUnitError(f"Неизвестная единица: {dst}")

    
    # определение группы (length, mass или temp) для обеих единиц
    group_src, _ = UNITS[src]
    group_dst, _ = UNITS[dst]

    
    # ошибка если группы разные и перевод невозможен
    if group_src != group_dst:
        raise IncompatibleUnitsError(f"Нельзя перевести {src} в {dst}")

    #  Перевод температур
    if group_src == "temp":
        # перевод исходной температуры в Кельвины
        if src == "c":
            k = value + 273.15
        elif src == "f":
            k = (value - 32) * 5 / 9 + 273.15
        else:
            k = value  # если уже в Кельвинах

        
        #ошибка если температура ниже абсолютного нуля
        if k < 0:
            raise BelowAbsoluteZeroError("Температура ниже абсолютного нуля")

        
        # перевод из Кельвинов в целевую единицу
        if dst == "c":
            return k - 273.15
        elif dst == "f":
            return (k - 273.15) * 9 / 5 + 32
        else:
            return k

    
    # Перевод длины и массы
    # Перевод в базовую единицу, затем из базовой в целевую
    return value * UNITS[src][1] / UNITS[dst][1]