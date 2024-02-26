# Корневой каталог проекта.

## Доступные команды.

### Линтеры.

- Black.
```bash
black --line-length=79 --target-version=py312 --skip-string-normalization --exclude="migrations" .
```

- Flake8
```bash
flake8 --config core/configs/flake8 .
```

- Isort.
```bash
isort --sp=core/configs/.isort.cfg .
```

### Тесты.
- Запуск тестов для backend.
```bash
python -m pytest -v --tb=short --config-file=core/configs/pytest.ini backend
```

- Запуск интеграционных тестов для backend.
```bash
python -m pytest -v --tb=short --config-file=core/configs/pytest.ini backend/tests/integration
```

- Запуск юнит тестов для backend.
```bash
python -m pytest -v --tb=short  --config-file=core/configs/pytest.ini backend/tests/unit 
```


### Миграции.
- Создать миграцию.
```bash
alembic --config=core/configs/alembic.ini revision -message="some message" --autogenerate
```

- Применить последнию миграцию.
```bash
alembic --config=core/configs/alembic.ini alembic upgrade head
```