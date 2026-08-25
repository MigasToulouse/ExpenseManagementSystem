# Expense Management System

An automated Expense Management System for households, designed to process receipts and generate comprehensive monthly expense reports, providing financial insights and improving budgeting efficiency.

## Getting Started

Run `make --help` for available options.

## Local env creation

See: [Set up python env](./guides/setup-dev-env.md) for details.

You should be able to create local dev env using your [conda](https://docs.conda.io/en/latest/miniconda.html)
installation.

## Docs

To build project documentation, run:

```shell
make docs
```

and then:

```shell
mkdocs serve
```

## Running tests

To run the unit tests, execute:

```shell
pytest tests -v
```
