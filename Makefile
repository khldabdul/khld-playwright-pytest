# Makefile for E2E Test Automation Framework

.PHONY: install install-dev install-browsers test test-smoke test-admin test-customer report clean help

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
	@echo "  make test-smoke       Run smoke tests only"
	@echo "  make test-admin       Run admin portal tests"
	@echo "  make test-customer    Run customer portal tests"
	@echo "  make test-headed      Run tests with visible browser"
	@echo ""
	@echo "  make report           Generate and open Allure report"
	@echo "  make report-serve     Serve Allure report on local server"
	@echo ""
	@echo "  make lint             Run linting"
	@echo "  make format           Format code"
	@echo "  make typecheck        Run type checking"
	@echo ""
	@echo "  make clean            Clean test artifacts"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-browsers:
	playwright install chromium
	playwright install firefox
	playwright install webkit

setup: install-dev install-browsers
	@echo "Setup complete!"

# Testing - all tests are in apps/ directory
test:
	pytest apps/ -v --alluredir=test-results/allure-results

test-smoke:
	pytest apps/ -v -m smoke --alluredir=test-results/allure-results

test-regression:
	pytest apps/ -v -m regression --alluredir=test-results/allure-results

test-admin:
	pytest apps/admin_portal/ -v --alluredir=test-results/allure-results

test-customer:
	pytest apps/customer_portal/ -v --alluredir=test-results/allure-results

test-headed:
	pytest apps/ -v --headed --alluredir=test-results/allure-results

test-debug:
	pytest apps/ -v --headed --slowmo=500 --alluredir=test-results/allure-results

test-staging:
	pytest apps/ -v --env staging --alluredir=test-results/allure-results

test-with-video:
	pytest apps/ -v --video=on --alluredir=test-results/allure-results

test-with-trace:
	pytest apps/ -v --tracing=on --alluredir=test-results/allure-results

# Parallel testing
test-parallel:
	pytest apps/ -v -n auto --alluredir=test-results/allure-results

# Reports
report:
	allure generate test-results/allure-results --clean -o test-results/allure-report
	allure open test-results/allure-report

report-generate:
	allure generate test-results/allure-results --clean -o test-results/allure-report

report-serve:
	allure serve test-results/allure-results

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
