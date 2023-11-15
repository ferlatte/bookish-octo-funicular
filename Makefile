PRE-COMMIT := $(shell which pre-commit)

all: run

clean:
	$(RM) .*.stamp

test:
	poetry run mypy .
	poetry run python3 -m unittest discover

run:
	poetry run ./main.py

pre-commit: .git/hooks/pre-commit
	pre-commit run --all-files

.git/hooks/pre-commit: $(PRE-COMMIT)
	pre-commit install

.PHONY: all clean run test pre-commit
