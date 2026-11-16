# Todos and Reminders API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

REST JSON API for managing todos on boards and for scheduling email reminders.
Built with Django REST Framework; delayed emails are sent by Celery.

## Features

- **Users**: registration and JWT authentication.
- **Boards**: create, list, rename and delete. Every user sees only their own boards.
  The list view returns `todo_count` (without todos); the detail view returns all
  todos (without `todo_count`).
- **Todos**: nested under a board. Add, list, change title or status, delete.
  Uncompleted todos are listed with `?done=false`.
- **Reminders**: an email address, a text and a delay in minutes. Celery sends the
  email after the delay. List, create and delete.
- **Docs**: OpenAPI schema, Swagger UI and ReDoc.

## Quick start (Docker)

Requirements: Docker with Compose v2.

```bash
git clone https://github.com/lisaevt/DRF_to_do_app.git
cd DRF_to_do_app
cp .env.example .env
docker compose up --build
```

Compose starts PostgreSQL, Redis, the web service (gunicorn, applies migrations on
start) and the Celery worker. When the logs settle, open:

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin: http://localhost:8000/admin/

Create an admin user (optional):

```bash
docker compose exec web python manage.py createsuperuser
```

Stop everything with `docker compose down` (add `-v` to also delete the data).

> `.env.example` contains placeholder secrets that are fine for a local run.
> Replace `SECRET_KEY` and `DB_PASSWORD` for anything else.

## Try it

```bash
# 1. Register and get a token
curl -X POST localhost:8000/api/auth/register/ -H "Content-Type: application/json" \
  -d '{"username":"lisa","email":"lisa@example.com","password":"S0me-Long-Pass!"}'

curl -X POST localhost:8000/api/auth/token/ -H "Content-Type: application/json" \
  -d '{"username":"lisa","password":"S0me-Long-Pass!"}'
# -> {"refresh": "...", "access": "<access>"}

# 2. Create a board and add a todo
curl -X POST localhost:8000/api/boards/ -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" -d '{"name":"Work"}'

curl -X POST localhost:8000/api/boards/1/todos/ -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" -d '{"title":"Write README"}'

# 3. List only uncompleted todos
curl "localhost:8000/api/boards/1/todos/?done=false" -H "Authorization: Bearer <access>"

# 4. Set a reminder for one minute from now
curl -X POST localhost:8000/api/reminders/ -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d '{"email":"me@example.com","text":"Call back","delay_minutes":1}'
```

With the default console email backend the reminder is printed in the worker log
after the delay:

```bash
docker compose logs -f worker
```

In Swagger UI, paste the `access` token into **Authorize** (no `Bearer` prefix needed).

## API overview

| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/token/` | Obtain access and refresh tokens |
| POST | `/api/auth/token/refresh/` | Refresh the access token |
| GET, POST | `/api/boards/` | List boards (with `todo_count`), create a board |
| GET, PUT, PATCH, DELETE | `/api/boards/{id}/` | Board detail (with todos), rename, delete |
| GET, POST | `/api/boards/{id}/todos/` | List todos of a board (`?done=false`), add a todo |
| GET, PUT, PATCH, DELETE | `/api/boards/{id}/todos/{todo_id}/` | Todo detail, change title or status, delete |
| GET, POST | `/api/reminders/` | List reminders, create a reminder |
| DELETE | `/api/reminders/{id}/` | Delete a reminder |
| GET | `/api/schema/`, `/api/docs/`, `/api/redoc/` | OpenAPI schema and docs |

All endpoints except registration, token and docs require authentication.
List endpoints are paginated (`?page=N`) and support `?search=` and `?ordering=`.

## Configuration

Settings are read from environment variables (see `.env.example`).

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key (required) |
| `DEBUG` | `True` or `False` |
| `ALLOWED_HOSTS` | Comma-separated host names |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | PostgreSQL credentials |
| `DB_HOST`, `DB_PORT` | PostgreSQL address. In Docker the web and worker services use `db:5432`; `DB_PORT` also sets the port published on your machine, change it if 5432 is taken |
| `CELERY_BROKER_URL` | Redis URL used by Celery |
| `EMAIL_BACKEND` | Defaults to the console backend, which prints emails to the log |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP settings, used with the SMTP backend |
| `EMAIL_USE_TLS`, `EMAIL_USE_SSL` | `True` or `False` (mutually exclusive) |
| `DEFAULT_FROM_EMAIL` | Sender address of reminder emails |
| `WEB_PORT`, `GUNICORN_WORKERS` | Optional: published port and number of gunicorn workers |

To send real emails, set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
and fill in the SMTP variables.

## Running without containers for the app

PostgreSQL and Redis still run in Docker; Django and the worker run locally.
Requires Python 3.12.

```bash
docker compose up -d db redis
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # DB_HOST=localhost, broker on localhost
python manage.py migrate
python manage.py runserver
```

In a second terminal:

```bash
celery -A config worker -l info
```

Dependencies are managed with pip-tools: edit `requirements.in`, then run
`pip-compile requirements.in`.

## Project structure

```
config/       settings, Celery app, root URLs
accounts/     custom User model, registration, JWT endpoints
todos/        Board and Todo: models, serializers, viewsets, routes
reminders/    Reminder model, API, Celery task, services
```

## Design notes

- **Data isolation.** Querysets are filtered by the current user, so a foreign board
  or reminder looks nonexistent (404) instead of forbidden (403). Todos are always
  reached through a board owned by the user; the board comes from the URL, never from
  the request body.
- **Response shapes.** Separate serializers for board list, detail and write, chosen
  in `get_serializer_class()`, match the required shapes. `todo_count` is a single
  `annotate` query and the detail view uses `prefetch_related`, so there are no
  N+1 queries.
- **Secure by default.** `IsAuthenticated` is the global default permission; public
  endpoints opt in explicitly.
- **Reminders.** The Celery task is scheduled with an absolute ETA inside
  `transaction.on_commit`, so a worker never sees a reminder that is not committed yet.
  The task receives only the reminder id and re-reads it: a reminder deleted before
  it fires is skipped, and a `sent_at` check plus a row lock prevent duplicate
  emails if the broker redelivers a task. Failed sends are retried with backoff.
- **Admin.** Reminders are read-only in the admin because tasks are scheduled by the
  API; an object added there would never be sent.

## Limitations

- The delay is limited to 24 hours (`REMINDER_MAX_DELAY` in settings). Redis
  redelivers tasks that are not acknowledged within its visibility timeout, so the
  timeout is raised above the maximum delay. For longer delays a periodic Celery beat
  task that polls the database would be the more robust design.
- Email delivery is at-least-once: if an email is sent but saving `sent_at` fails,
  a retry sends it again. The row stays locked while the SMTP request runs.
- Migrations are applied on start of the web container. That is convenient for a
  one-command start; in production they would be a separate deployment step.
- The assignment mentions both `name` and `title` for a board; the field is `name`.
- Automated tests are not included.

## Development workflow

Work is done in short feature branches (`chore/setup`, `feat/accounts`, `feat/todos`,
`feat/reminders`, ...) merged into `main` with merge commits. Commit messages follow
[Conventional Commits](https://www.conventionalcommits.org/).