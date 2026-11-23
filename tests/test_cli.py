"""Тесты CLI: запуск как отдельный процесс"""

import subprocess
import sys


def run(*args):
    """Запуск CLI с указанными аргументами и возвращение результата """
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
    )


def test_help():
    """--help показывает подкоманды и завершается с кодом 0."""
    r = run("--help")
    assert r.returncode == 0
    assert "calc" in r.stdout
    assert "convert" in r.stdout


def test_calc_success():
    """Успешный calc: код 0, результат в stdout"""
    r = run("calc", "2+3*4")
    assert r.returncode == 0
    assert r.stdout.strip() == "14.0"


def test_calc_error():
    """Ошибка в calc: код 2, сообщение в stderr"""
    r = run("calc", "2+a")
    assert r.returncode == 2
    assert r.stderr
    assert "error" in r.stderr.lower() or "ошибка" in r.stderr.lower()


def test_convert_success():
    """Успешный convert: код 0, результат в stdout"""
    r = run("convert", "1000", "--from", "mm", "--to", "m")
    assert r.returncode == 0
    assert float(r.stdout.strip()) == 1.0