.PHONY: help install install-dev test lint format type-check clean run

help:
	@echo "Available commands:"
	@echo "  install      Install project dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests with coverage"
	@echo "  lint         Run ruff linter"
	@echo "  format       Format code with ruff"
	@echo "  type-check   Run mypy type checker"
	@echo "  clean        Clean up cache and build files"
	@echo "  run          Run the application"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests

type-check:
	mypy src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	rm -rf build dist *.egg-info

run:
	python -m transcription_tool