# Makefile for E2E Test Automation Framework

# Virtual environment path
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(PYTHON) -m pytest
PLAYWRIGHT := $(VENV)/bin/playwright

.PHONY: install install-dev install-browsers test test-smoke test-sauce-demo test-the-internet report clean help

# Default target
help:
	@echo "E2E Test Automation Framework"
	@echo ""
	@echo "Usage:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo "  make install-browsers Install Playwright browsers"
	@echo ""
	@echo "  make test             Run all tests"
	@echo "  make test ARGS='...'  Run tests with custom arguments"
	@echo "  make test-api         Run API tests (parallel)"
	@echo "  make test-e2e         Run E2E tests"
	@echo "  make test-smoke       Run smoke tests only"
	@echo "  make test-smoke-fast  Run smoke tests (parallel, no Allure)"
	@echo "  make test-sauce-demo  Run Sauce Demo tests"
	@echo "  make test-the-internet Run The Internet tests"
	@echo "  make test-headed      Run tests with visible browser"
	@echo "  make test-parallel    Run tests in parallel"
	@echo ""
	@echo "  make report           Generate and open Allure report"
	@echo "  make report-serve     Serve Allure report on local server"
	@echo ""
	@echo "  make lint             Run linting"
	@echo "  make format           Format code"
	@echo "  make typecheck        Run type checking"
	@echo ""
	@echo "  make clean            Clean test artifacts"
	@echo ""
	@echo "Examples:"
	@echo "  make test ARGS='apps/e2e/sauce_demo/tests/e2e/test_login.py'"
	@echo "  make test ARGS='-k \"test_login\" -v'"
	@echo "  make test ARGS='--headed'"

# Installation
install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

install-browsers:
	$(PLAYWRIGHT) install chromium
	$(PLAYWRIGHT) install firefox
	$(PLAYWRIGHT) install webkit

setup: install-dev install-browsers
	@echo "Setup complete!"

# Testing - all tests are in apps/ directory
# Usage: make test ARGS='your pytest arguments here'
test:
	mkdir -p allure-results
	$(PYTEST) apps/ --alluredir=allure-results $(ARGS)

test-smoke:
	mkdir -p allure-results
	$(PYTEST) apps/ -m smoke --alluredir=allure-results

test-regression:
	mkdir -p allure-results
	$(PYTEST) apps/ -m regression --alluredir=allure-results

test-sauce-demo:
	mkdir -p allure-results
	$(PYTEST) apps/e2e/sauce_demo/ --alluredir=allure-results

test-the-internet:
	mkdir -p allure-results
	$(PYTEST) apps/e2e/the_internet/ --alluredir=allure-results

test-headed:
	mkdir -p allure-results
	$(PYTEST) apps/ --headed --alluredir=allure-results

test-debug:
	mkdir -p allure-results
	$(PYTEST) apps/ --headed --slowmo=500 --alluredir=allure-results

test-staging:
	mkdir -p allure-results
	$(PYTEST) apps/ --env staging --alluredir=allure-results

test-with-video:
	mkdir -p allure-results
	$(PYTEST) apps/ --video=on --alluredir=allure-results

test-with-trace:
	mkdir -p allure-results
	$(PYTEST) apps/ --tracing=on --alluredir=allure-results

# API and E2E specific
test-api:
	mkdir -p allure-results
	$(PYTEST) apps/api/ -n auto --alluredir=allure-results

test-e2e:
	mkdir -p allure-results
	$(PYTEST) apps/e2e/ --alluredir=allure-results

test-smoke-fast:
	$(PYTEST) -m smoke -n auto --tb=short

# Parallel testing
test-parallel:
	mkdir -p allure-results
	$(PYTEST) apps/ -n auto --alluredir=allure-results

# Reports
report:
	@echo "Generating Allure report with history..."
	@if [ -d "test-results/allure-history" ]; then \
		cp -r test-results/allure-history allure-results/history; \
	fi
	allure generate allure-results -o test-results/allure-report
	@if [ -d "allure-results/history" ]; then \
		rm -rf test-results/allure-history && \
		cp -r allure-results/history test-results/allure-history; \
	fi
	allure open test-results/allure-report

report-generate:
	@echo "Generating Allure report with history..."
	@if [ -d "test-results/allure-history" ]; then \
		cp -r test-results/allure-history allure-results/history; \
	fi
	allure generate allure-results -o test-results/allure-report
	@if [ -d "allure-results/history" ]; then \
		rm -rf test-results/allure-history && \
		cp -r allure-results/history test-results/allure-history; \
	fi

report-serve:
	@echo "Serving Allure report with history..."
	@if [ -d "test-results/allure-history" ]; then \
		cp -r test-results/allure-history allure-results/history; \
	fi
	allure serve allure-results

report-clean:
	allure generate allure-results --clean -o test-results/allure-report
	@echo "Report generated without history (clean mode)"

# Code quality
lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy .

check: lint typecheck
	@echo "All checks passed!"

# Cleanup
clean:
	rm -rf test-results/
	rm -rf .pytest_cache/
	rm -rf **/__pycache__/
	rm -rf *.egg-info/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

clean-reports:
	rm -rf test-results/allure-results/
	rm -rf test-results/allure-report/
	rm -rf test-results/screenshots/
	rm -rf test-results/traces/
	rm -rf test-results/videos/
	@echo "Note: test-results/allure-history/ preserved for test history tracking"

clean-all:
	rm -rf test-results/
	rm -rf allure-results/
	rm -rf .pytest_cache/
	rm -rf **/__pycache__/
	rm -rf *.egg-info/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
