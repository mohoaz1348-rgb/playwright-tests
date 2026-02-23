import shutil
import sys
import pytest
import os
import subprocess
from pathlib import Path


def run_tests():
    # Очистка прошлых результатов тестов
    results_dir = Path("results")
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(exist_ok=True)

    # Установка браузеров (uv run чтобы не заходить в venv)
    # Если браузеры есть, это пройдет мгновенно
    # subprocess.run(["uv", "run", "playwright", "install", "chromium"])

    # Забираем все аргументы командной строки
    args = sys.argv[1:]

    # Проверяем наш кастомный флаг
    # Если он есть, запоминаем и удаляем его из списка для Pytest
    serve_report = "--no-serve" not in args
    if not serve_report:
        args.remove("--no-serve")
        
    #docker build -t playwright-uv . 
    subprocess.run(["docker", "build", "-t", "playwright-uv", "."])
    #docker run -u $(id -u):$(id -g) -v $(pwd)/results:/app/results:rw --rm playwright-uv
    current_dir = os.getcwd()

    command = (
        f"docker run -u $(id -u):$(id -g) "
        f"-v {current_dir}/results:/app/results:rw "
        f"--rm playwright-uv:latest uv run pytest -o cache_dir=results/.pytest_cache {' '.join(args)}"
    )

    print("Запуск тестов в Docker...")
    result = subprocess.run(command, shell=True, check=True, text=True)

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

    #sys.exit(exit_code)
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_tests()
