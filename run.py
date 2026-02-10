import shutil
import sys
import pytest
import subprocess
from pathlib import Path


def run_tests():
    # Очистка прошлых результатов тестов
    results_dir = Path("results")
    if results_dir.exists():
        shutil.rmtree(results_dir)

    # Установка браузеров (uv run чтобы не заходить в venv)
    # Если браузеры есть, это пройдет мгновенно
    subprocess.run(["uv", "run", "playwright", "install", "chromium"])

    # Забираем все аргументы командной строки
    args = sys.argv[1:]

    # Проверяем наш кастомный флаг
    # Если он есть, запоминаем и удаляем его из списка для Pytest
    serve_report = "--no-serve" not in args
    if not serve_report:
        args.remove("--no-serve")

    # Теперь Pytest получит только те флаги, которые он понимает
    exit_code = pytest.main(args)

    # Используем наш параметр запуска тестов для логики Allure
    allure_results = results_dir / "allure-results"
    if serve_report and allure_results.exists():
        print("\n=== Генерирую отчет Allure (Ctrl+C для выхода)... ===")
        try:
            # Запускаем сервер
            subprocess.run(["allure", "serve", str(allure_results)])
        except KeyboardInterrupt:
            # Ловим прерывание, чтобы не выводить ошибку в консоль
            print("\n[INFO] Сервер Allure остановлен пользователем.")
        except Exception as e:
            print(f"\n[ERROR] Не удалось запустить Allure: {e}")

    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()
