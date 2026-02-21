import subprocess
import shutil
import sys
import pytest
from pathlib import Path

if __name__ == "__main__":
    # Очистка папки с результатами перед стартом тестов
    results_dir = Path("results")
    if results_dir.exists():
        shutil.rmtree(results_dir)

    # Проверяем и устанавливаем браузеры (playwright сделает это быстро, если они уже есть)
    # Используем "uv run", чтобы не привязываться к окружению
    # subprocess.run(["uv", "run", "playwright", "install", "chromium"])

    # Запуск pytest с передачей всех аргументов из командной строки
    sys.exit(pytest.main(sys.argv[1:]))
