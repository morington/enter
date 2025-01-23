from pathlib import Path

# Получаем путь к текущему файлу __init__.py
current_dir = Path(__file__).parent

# Путь к template.html относительно текущего файла
ERROR_TEMPLATE_PATH = current_dir / 'error_base' / 'template.html'