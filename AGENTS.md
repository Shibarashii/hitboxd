# AGENTS.md — Hitboxd Project Instructions

## Project Overview

**Hitboxd** is a video game tracking, diary, and review web application inspired by Letterboxd.

The project is built in two distinct phases:
* **Phase 1 (Current):** Pure Django — server-rendered templates, Django forms, session authentication, and PostgreSQL. No JS frameworks or DRF endpoints in Phase 1.
* **Phase 2 (Future):** DRF REST API + React frontend — exposing the same backend models through Django REST Framework consumed by a separate React app.

> **Crucial Working Mode:**  
> The human developer writes the code. The AI assistant acts as a **Senior Pair Programmer, Architect, and Code Reviewer** — answering questions, stress-testing design decisions, helping with API integration, and reviewing code against best practices. Do not write unsolicited full-file implementations unless explicitly asked.

---

## Tech Stack

* **Language:** Python 3.14
* **Web Framework:** Django 6.1+
* **Database:** PostgreSQL (using `psycopg` / `psycopg2-binary`)
* **External Game API:** RAWG Video Games Database API (`https://api.rawg.io/api/`)
* **Environment Variables:** Handled via `python-dotenv` (`.env`)

---

## App Structure & Responsibilities

```
Hitboxd/
├── users/       # Identity, auth, profile metadata, social graph, featured favorites
├── games/       # Local cache of game data, genres, RAWG API client
└── reviews/     # Game logs (status, 1-5 rating) and attached written reviews
```

### Models & Relational Boundaries

1. **`users` app:**
   * `User`: Extends `AbstractUser`. Registered as `AUTH_USER_MODEL = 'users.User'`.
   * `UserProfile`: `OneToOneField` with `User`, stores `bio` and `avatar_url`.
   * `Follow`: Social graph tracking `follower` and `following` with a `unique_follow` constraint.
   * `FeaturedGame`: Ordered list of up to 4 pinned favorite games (`position` 1–4) with uniqueness per slot and per game.

2. **`games` app:**
   * `Genre`: Local cache of game genres (`name`, `slug`, optional `rawg_id`).
   * `Game`: Local cache of RAWG game data (`rawg_id`, `name`, `slug`, `cover_url`, `first_release_date`, `summary`, `genres` M2M).

3. **`reviews` app:**
   * `LogEntry`: User-game interaction (`user`, `game`, `status`, optional `rating` 1–5). Exactly **one** log entry per user per game (`unique_user_game_log`).
   * `Review`: `OneToOneField` with `LogEntry`. A user can only review a game they have logged.

---

## Architecture Rules & Conventions

* **Cross-App Model References:**
  Always use string references to avoid circular imports:
  * For User: `settings.AUTH_USER_MODEL` or `"users.User"`
  * For Game: `"games.Game"`
* **External API Strategy:**
  `Game` is a local cache. First time a game is referenced from RAWG, fetch and save it to the local PostgreSQL database. Subsequent reads query the local DB only.
* **URLs:**
  Game detail pages route strictly by slug: `/games/<slug>/`.
* **Database Constraints:**
  Always enforce relational and business rules at the database level (`models.UniqueConstraint`, `models.CheckConstraint`, validators) in addition to form/view validation.
* **Timestamps:**
  Use `created_at = models.DateTimeField(auto_now_add=True)` and `updated_at = models.DateTimeField(auto_now=True)`.

---

## Essential Commands

```bash
# Run server
python manage.py runserver

# System checks
python manage.py check

# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Testing
python manage.py test
```

---

## Required Environment Variables (`.env`)

Copy `.env.example` to `.env` and fill in:

```env
DJANGO_SECRET_KEY=your_django_secret_key
DEBUG=True
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
RAWG_API_KEY=your_rawg_api_key
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

`DEBUG` is only on when the value is the string `true` (case-insensitive); a missing value means off. The database name (`hitboxd`, on `localhost:5432`) is still hardcoded in `Hitboxd/settings.py`.

---

## Documentation Index

* [`docs/ideas/hitboxd.md`](docs/ideas/hitboxd.md) — Product vision, MVP scope, and "Not Doing" boundaries.
* [`docs/schema.md`](docs/schema.md) — Complete database schema reference and field mappings.
* [`docs/ui.md`](docs/ui.md) — Planned UI layouts, pages, and interactive features.
* [`tasks/plan.md`](tasks/plan.md) — Implementation architecture, dependency graph, and risks.
* [`tasks/todo.md`](tasks/todo.md) — Ordered task checklist and checkpoints for Phase 1.
