PRE-COMMIT := $(shell which pre-commit)

all: run

clean:
	$(RM) .*.stamp

test:
	mypy .
	python3 -m unittest discover

run:
	./main.py
pre-commit: .git/hooks/pre-commit
	pre-commit run --all-files

.git/hooks/pre-commit: $(PRE-COMMIT)
	pre-commit install

.PHONY: all clean run test pre-commit
