SHELL := /bin/bash

# Pre-commit.
install-pre-commit:
	source .venv/bin/activate && pre-commit install -c fastapi_backend/core/configs/.pre-commit-config.yaml

uninstall-pre-commit:
	source .venv/bin/activate && pre-commit uninstall

run-pre-commit:
	source .venv/bin/activate && pre-commit run -c fastapi_backend/core/configs/.pre-commit-config.yaml


# Linters.
run_black:
	source .venv/bin/activate && black --line-length=79 --target-version=py312 --skip-string-normalization .

run-flake8:
	source .venv/bin/activate && flake8 --config fastapi_backend/core/configs/flake8 .

run-isort:
	source .venv/bin/activate && isort --sp=fastapi_backend/core/configs/.isort.cfg .

# Tests.
run-all-tests:
	source .venv/bin/activate && pytest	-v	--tb=short	--config-file=fastapi_backend/core/configs/pytest.ini

run-only-integration-tests:
	source .venv/bin/activate && pytest	-v	--tb=short	--config-file=fastapi_backend/core/configs/pytest.ini tests/integration

run-only-unit-tests:
	source .venv/bin/activate && pytest	-v	--tb=short	--config-file=fastapi_backend/core/configs/pytest
	.ini fastapi_backend/backend/tests/unit

# Migrations.
make_migration:
	source .venv/bin/activate && alembic --config=fastapi_backend/core/configs/alembic.ini revision --autogenerate

upgrade:
	source .venv/bin/activate && alembic --config=fastapi_backend/core/configs/alembic.ini upgrade 15fc955565a4
