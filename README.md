# Wishlist Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP26-003/wishlists/branch/master/graph/badge.svg)](https://codecov.io/gh/CSCI-GA-2820-SP26-003/wishlists)

## Overview
This Wishlist service is a REST API for managing wishlists and wishlist items. This code is modeled after the sample-accounts code which can be found [sample-accounts](https://github.com/nyu-devops/sample-accounts).

## What this service does

- Create, list, read, update, and delete wishlists
- List items in a wishlist
- Create and read items in a wishlist
- Filter wishlists by `customer_id` or `name`

## Quick Start
** If you use Mac Finder or Windows Explorer you will need to copy:
```
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

### 1) Install dependencies
```bash
make install
```
### 2) Initialize the database
```bash
flask db-create
```
### 3) Run the service
```bash
make run
```

### 4) Run tests
```bash
make test
```

## API Endpoints

Base resource: `/wishlists`

### Wishlists

| Method | Path | Description |
|---|---|---|
| GET | `/wishlists` | List wishlists |
| POST | `/wishlists` | Create a wishlist |
| GET | `/wishlists/{wishlist_id}` | Get one wishlist |
| PUT | `/wishlists/{wishlist_id}` | Update wishlist name/description |
| DELETE | `/wishlists/{wishlist_id}` | Delete a wishlist |

### Wishlist Items

| Method | Path | Description |
|---|---|---|
| GET | `/wishlists/{wishlist_id}/items` | List items in a wishlist |
| POST | `/wishlists/{wishlist_id}/items` | Create an item in a wishlist |
| GET | `/wishlists/{wishlist_id}/items/{item_id}` | Get one item in a wishlist |
| PUT | `/wishlists/{wishlist_id}/items/{item_id}` | Update item in wishlist |
| DELETE | `/wishlists/{wishlist_id}/items/{item_id}` | Deletes item in a wishlist |

## Project Layout

```text
.gitignore                  - ignore Git metadata and local artifacts
.flaskenv                   - Flask environment defaults
.gitattributes              - git text/binary attributes
.devcontainer/              - VS Code dev container config
dot-env-example             - example environment variables file
LICENSE                     - Apache 2.0 license
Makefile                    - common development commands
Pipfile                     - Python dependencies
Procfile                    - process definition for running app
setup.cfg                   - tool configuration (lint/test)
wsgi.py                     - WSGI entrypoint

service/
├── __init__.py                - package initializer
├── routes.py                  - API routes
├── config.py                  - configuration parameters
├── common/
│   ├── cli_commands.py        - Flask command to recreate all tables
│   ├── error_handlers.py      - HTTP error handling code
│   ├── log_handlers.py        - logging setup code
│   └── status.py              - HTTP status constants
└── models/
    ├── __init__.py
    ├── wishlist.py            - Database model for Wishlist
    ├── item.py                - Database model for Item
    └── persistent_base.py

tests/                          - test cases package
├── __init__.py                 - package initializer
├── test_routes.py              - Factory for testing with fake objects
├── test_wishlist_model.py      - test suite for the CLI
├── test_item_model.py          - test suite for business models
└── test_cli_commands.py        - test suite for service routes
```

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
