# bookish-octo-funicular
Convert calendars into a schedule.

## CI Status
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ferlatte/bookish-octo-funicular/main.svg)](https://results.pre-commit.ci/latest/github/ferlatte/bookish-octo-funicular/main)


## Setup
You will need `asdf` and `pre-commit` installed already.

```sh
asdf install
asdf reshim
pip3 install --upgrade pip
pip3 install poetry
asdf reshim # Need to run this again to get poetry into the PATH
make installdeps
make test
```

## Dependencies

### Adding a new Python dependency
```
poetry add name_of_package
poetry add name_of_dev_package --group dev
```
Note that pre-commit's mypy hook will need any module type stub packages added to additional_dependencies after you install them via poetry.

### Updating dependencies
Do this regularly.

```
poetry update
asdf latest
```
