.PHONY: all format lint test tests test_watch integration_tests docker_tests help extended_tests install update clean spell_check spell_fix jupyter

# Default target executed when no arguments are given to make.
all: help

# Define a variable for the test file path.
TEST_FILE ?= tests/unit_tests/

test:
	uv run pytest $(TEST_FILE)

integration_tests:
	uv run pytest tests/integration_tests 

test_watch:
	uv run ptw --snapshot-update --now . -- -vv tests/unit_tests

test_profile:
	uv run pytest -vv tests/unit_tests/ --profile-svg

extended_tests:
	uv run pytest --only-extended $(TEST_FILE)


######################
# LINTING AND FORMATTING
######################

# Define a variable for Python and notebook files.
PYTHON_FILES=src/
MYPY_CACHE=.mypy_cache
lint format: PYTHON_FILES=.
lint_diff format_diff: PYTHON_FILES=$(shell git diff --name-only --diff-filter=d main | grep -E '\.py$$|\.ipynb$$')
lint_package: PYTHON_FILES=src
lint_tests: PYTHON_FILES=tests
lint_tests: MYPY_CACHE=.mypy_cache_test

lint lint_diff lint_package lint_tests:
	uv run ruff check .
	[ "$(PYTHON_FILES)" = "" ] || uv run ruff format $(PYTHON_FILES) --diff
	[ "$(PYTHON_FILES)" = "" ] || uv run ruff check --select I $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || uv run mypy --strict $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || mkdir -p $(MYPY_CACHE) && uv run mypy --strict $(PYTHON_FILES) --cache-dir $(MYPY_CACHE)

format format_diff:
	uv run ruff format $(PYTHON_FILES)
	uv run ruff check --select I --fix $(PYTHON_FILES)

spell_check:
	uv run codespell --toml pyproject.toml

spell_fix:
	uv run codespell --toml pyproject.toml -w

######################
# UV PROJECT MANAGEMENT
######################

install:
	uv sync --all-extras --dev

update:
	uv lock --upgrade

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

######################
# HELP
######################

help:
	@echo '----'
	@echo 'UV Project Management:'
	@echo 'install                      - install all dependencies with uv'
	@echo 'update                       - update dependencies lock file'
	@echo 'clean                        - remove cache and temp files'
	@echo ''
	@echo 'Testing:'
	@echo 'test                         - run unit tests'
	@echo 'integration_tests            - run integration tests'
	@echo 'test TEST_FILE=<test_file>   - run all tests in file'
	@echo 'test_watch                   - run unit tests in watch mode'
	@echo ''
	@echo 'Code Quality:'
	@echo 'format                       - run code formatters'
	@echo 'lint                         - run linters'
	@echo 'spell_check                  - check spelling'
	@echo 'spell_fix                    - fix spelling errors'
	@echo ''
	@echo 'Development:'
	@echo 'dev                          - run langgraph dev server'
	@echo 'jupyter                      - run jupyter lab without browser'



dev:
	uv run langgraph dev

jupyter:
	uv run jupyter lab --no-browser