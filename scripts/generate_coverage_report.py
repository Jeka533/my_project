#!/usr/bin/env python3
"""
Скрипт для генерации отчета о покрытии кода тестами.
"""
import os
import shutil
import subprocess
import sys
from typing import Optional


def generate_coverage_report() -> bool:
    """Генерирует HTML отчет о покрытии тестами."""

    print("=" * 60)
    print("Генерация отчета о покрытии тестами")
    print("=" * 60)

    # Убедимся, что мы в правильной директории
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    print(f" Рабочая директория: {base_dir}")
    print(" Директория с исходным кодом: src/")

    # Очистим предыдущие отчеты
    print("\n 1. Очистка предыдущих отчетов...")
    if os.path.exists("coverage_html"):
        shutil.rmtree("coverage_html")
    if os.path.exists(".coverage"):
        os.remove(".coverage")

    # Установим необходимые пакеты
    print("\n 2. Проверка и установка необходимых пакетов...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "pytest-cov", "coverage"],
                   capture_output=True)

    # Запустим тесты с измерением покрытия
    print("\n 3. Запуск тестов с измерением покрытия...")
    result: subprocess.CompletedProcess = subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:coverage_html",
        "-v",
        "tests/"
    ], capture_output=True, text=True)

    print("\n" + "=" * 40)
    print("Результаты тестов:")
    print("=" * 40)
    print(result.stdout)

    if result.stderr:
        print("\n  Предупреждения/Ошибки:")
        print(result.stderr)

    # Проверим, есть ли данные о покрытии
    if os.path.exists(".coverage"):
        print("\n Файл с данными покрытия создан")

        # Покажем отчет о покрытии
        cov_result: subprocess.CompletedProcess = subprocess.run([
            sys.executable, "-m", "coverage", "report"
        ], capture_output=True, text=True)

        print("\n Отчет о покрытии:")
        print(cov_result.stdout)

        # Проверим процент покрытия
        if cov_result.stdout:
            import re
            match: Optional[re.Match] = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', cov_result.stdout)
            if match:
                coverage_pct: int = int(match.group(1))
                if coverage_pct >= 80:
                    print(f"\n Покрытие кода тестами {coverage_pct}% - отлично!")
                else:
                    print(f"\n⚠  Покрытие кода тестами {coverage_pct}% - менее 80%")
    else:
        print("\n Файл с данными покрытия не создан")

    html_index: str = os.path.join("coverage_html", "index.html")
    if os.path.exists(html_index):
        abs_path: str = os.path.abspath(html_index)
        print("\n HTML отчет о покрытии доступен по пути:")
        print(f"   file://{abs_path}")
        return True
    else:
        print("\n HTML отчет не был создан")
        return False


if __name__ == "__main__":
    success: bool = generate_coverage_report()
    sys.exit(0 if success else 1)
