# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

The imported `AGENTS.md` is the primary project brief (working mode, stack, models, conventions). The notes below add what it doesn't cover.

## Working mode reminder

The human writes the code; act as pair programmer / architect / reviewer. Don't produce full-file implementations unless asked.

## Commands

The venv lives in `.venv/` (activate it, or prefix commands with `.venv/bin/`). To set up a new checkout, copy `.env.example` to `.env` and generate a `DJANGO_SECRET_KEY` (see `AGENTS.md`). Note the variable is `DJANGO_SECRET_KEY`, not `SECRET_KEY`; if it's missing, Django fails at startup because `SECRET_KEY` is empty.

```bash
python manage.py test                                   # all tests
python manage.py test reviews                           # one app
python manage.py test reviews.tests.LogEntryTests       # one TestCase
python manage.py test reviews.tests.LogEntryTests.test_x  # one method
ruff check .                                            # lint (config in pyproject.toml; RUF012 ignored)
pyright                                                 # type check (django-stubs installed; see pyrightconfig.json)
```

`ruff` and `pyright` aren't in `requirements.txt`. They're installed globally through Neovim's Mason.

Tests run against PostgreSQL (the only configured DB), so the Postgres user needs `CREATEDB` permission for Django's test database.

## Current state

- Only models + admin registrations exist so far. No `urls.py` per app, no views, no forms, no `templates/` directory yet; `Hitboxd/urls.py` only routes `admin/`. Progress is tracked in `tasks/todo.md`.
- The game API switched from IGDB to RAWG (commit `8f84360`). The docs have been updated to match, but if an IGDB reference turns up, the models are the source of truth.
- `RAWG_API_KEY` is in `.env` but not yet read into `settings.py`; the planned client is `games/rawg.py` (Task 4).
- `ALLOWED_HOSTS` is `[]`, which only works while `DEBUG` is on. Running with `DEBUG=False` locally returns 400s until `localhost`/`127.0.0.1` are added.
- `db.sqlite3` in the repo root is a leftover; the app uses PostgreSQL.
- `django-debug-toolbar` is in `INSTALLED_APPS` and middleware, but its URLs aren't included yet.

## Planned conventions (from `tasks/plan.md`)

- **Class-based views by default** (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `LoginView`, etc.). Use FBVs only where CBVs don't fit, such as the log-entry upsert, and note the reason inline.
- Templates go in a top-level `templates/` dir (`templates/base.html`, `templates/<app>/...`), registered in `TEMPLATES[0]['DIRS']`.
- Logging a game is an upsert on `LogEntry` (one per user+game), not a new row.
- Status choices live in `reviews.models.Status` (`played`, `playing`, `want`).
