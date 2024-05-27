PRE-COMMIT := $(shell which pre-commit)

all: run

clean:
	$(RM) .*.stamp

test: poetry.lock
	poetry run mypy .
	poetry run python3 -m unittest discover

# The default flask port (5000) is used on macOS
run: poetry.lock
	poetry run python3 -m flask --app main run --port 5001 --debug

installdeps:
	pre-commit install
	poetry install

pre-commit: .git/hooks/pre-commit
	pre-commit run --all-files

poetry.lock: pyproject.toml
	poetry install
	touch poetry.lock # poetry install doesn't reliably update the lockfile when run

.git/hooks/pre-commit: $(PRE-COMMIT)
	pre-commit install

.PHONY: all clean run test pre-commit installdeps
