.PHONY: test build clean upload-test upload install-build-deps install-upload-deps install-dev-deps install-test-deps format lint typecheck generate-from-docs install-setuptools

VENV_PYTHON := ./.venv/bin/python
VENV_PIP := ./.venv/bin/pip

# Ensure the virtual environment is set up and activated for commands
# This ensures that all commands use the python and pip from the venv
check_venv:
	@if [ ! -f $(VENV_PYTHON) ]; then echo "Virtual environment not found. Please run 'python3 -m venv .venv' and then 'source .venv/bin/activate'."; exit 1; fi

install-setuptools: check_venv
	$(VENV_PIP) install setuptools

install-build-deps: check_venv install-setuptools
	$(VENV_PIP) install build

install-upload-deps: check_venv install-setuptools
	$(VENV_PIP) install twine

install-dev-deps: check_venv install-setuptools
	$(VENV_PIP) install -e . # Install the project in editable mode

install-test-deps: check_venv install-setuptools install-dev-deps
	$(VENV_PIP) install black flake8 mypy # Explicitly install test dependencies

test: check_venv install-test-deps lint typecheck
	rm -rf tests/output
	PYTHONPATH=src $(VENV_PYTHON) -m unittest discover -s tests/ -p '*_test.py'
	git diff --exit-code tests/output

format: check_venv install-test-deps
	$(VENV_PYTHON) -m black src/ tests/

lint: check_venv install-test-deps
	$(VENV_PYTHON) -m flake8 src/ tests/

typecheck: check_venv install-test-deps
	$(VENV_PYTHON) -m mypy src/ tests/

generate-from-docs: check_venv install-dev-deps
	@[ -z "$$(git status --porcelain src)" ] || (echo -n "Changes detected in 'src/', are you sure you want to continue? [y/N] " && read ans && [ "$${ans:-N}" = "y" ] || [ "$${ans:-N}" = "Y" ] || (echo "Aborting."; exit 1))
	./.venv/bin/md-tangle -v -f -p 2 DOCS.md

build: check_venv install-build-deps clean
	$(VENV_PYTHON) -m build

clean:
	@echo "Cleaning up build artifacts..."
	rm -rf dist/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.orig" -delete

upload-test: check_venv install-upload-deps build
	$(VENV_PYTHON) -m twine upload --repository testpypi dist/*

upload: check_venv install-upload-deps build
	$(VENV_PYTHON) -m twine upload dist/*
