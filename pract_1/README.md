# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```bash
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей и запуске
Тесты не требуют внешних зависимостей - pytest

# Создайте виртуальное окружение
python -m venv venv

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
pip install pytest
```

## Запуск
```bash
python main.py config.json
```

# 3. Структура проекта
Проект содержит следующие файлы и директории, связанные с тестированием:
```bash
commands.py           # Файл с реализацией команд
test_commands.py      # Файл с тестами для команд
```

# 4. Запуск тестов
В этом руководстве описывается, как запустить тесты для команд эмулятора оболочки. Мы будем использовать модуль Python `pytest -v` для тестирования.
```bash
pytest -v
```
