.PHONY: clean clean-test clean-pyc lint reformat test server help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-test ## Удалить все артефакты
	rm -f .coverage

clean-pyc: ## Удалить артефакты компиляции
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Удалить артефакты тестирования
	rm -fr .pytest_cache
	rm -fr .mypy_cache

lint: ## Проверить код с помощью ruff
	poetry run ruff api tests

reformat: ## Форматировать код с помощью black
	poetry run black --config pyproject.toml api tests

test: ## Запустить тесты
	poetry run pytest

server: ## Запустить сервер FastAPI
	uvicorn api.main:api --reload --port=8008 --workers 3