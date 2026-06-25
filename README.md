# Taskmanager API

## Local setup

1. Create a Python venv and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and update credentials:
   ```bash
   cp .env.example .env
   ```

3. Update `.env` with your Postgres or Supabase connection values.

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the app:
   ```bash
   uvicorn main:app --reload
   ```

6. Open API docs at `http://127.0.0.1:8000/docs`

## GitHub + Render deployment

- Push the project to GitHub.
- In Render, create a new Python web service.
- Use `pip install -r requirements.txt` as the build command.
- Use `uvicorn main:app --host 0.0.0.0 --port $PORT` as the start command.
- Add environment variables in Render: `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `ALEMBIC_DATABASE_URL`.

## Environment variables

- `DATABASE_URL` — async Postgres URL for the app
- `ALEMBIC_DATABASE_URL` — sync Postgres URL for Alembic
- `SECRET_KEY` — JWT secret
- `ALGORITHM` — JWT algorithm, default `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token expiry minutes, default `60`

## Notes

- The default signup route is `POST /register`.
- The login route is `POST /login`.
- The tasks routes require Bearer auth with the JWT access token.
