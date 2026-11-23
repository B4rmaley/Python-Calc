"""CLI toolkit: calc, convert, --help
Коды возврата:
    0 — успех
    2 — пользовательская ошибка (вывод в stderr)
"""

import sys
import argparse
from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main() -> None:
    """Точка входа CLI.
    Разбирает аргументы, вызывает соответствующую команду (calc или convert) и выводит результат
    При доменной ошибке сообщение выводится в stderr, процесс завершается с кодом 2
    """
    # создаётся главный парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Калькулятор и конвертер")

    # создаются подкоманды (calc и convert)
    subparsers = parser.add_subparsers(dest="command", required=True)

    # настройка calc
    p_calc = subparsers.add_parser("calc")
    p_calc.add_argument("expr", type=str)  # Обязательный аргумент - выражение

    # Настройка convert
    p_conv = subparsers.add_parser("convert")
    p_conv.add_argument("value", type=float)  # Обязательный аргумент - число
    p_conv.add_argument("--from", dest="from_unit", required=True)  # флаг --from
    p_conv.add_argument("--to", dest="to_unit", required=True)      # флаг --to

    # чтение аргументов, введёных пользователем
    args = parser.parse_args()

    try:
        # вызов calc
        if args.command == "calc":
            print(calculate(args.expr))
        # вызов convert
        elif args.command == "convert":
            print(convert(args.value, args.from_unit, args.to_unit))
    except ToolkitError as e:
        # Перехватывается любая доменная ошибка
        # Сообщение выводится в поток ошибок (stderr), процесс завершается с кодом 2
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()