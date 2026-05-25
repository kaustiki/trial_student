# Codex Handoff Guide

This project is the Student Care Referral System MVP. A new Codex session should
start here before changing code.

## Read First

1. `todo.md` - source of truth for what phase/task to complete next.
2. `requirements.md` - functional and non-functional requirements.
3. `plan.md` - product workflow and role responsibilities.
4. `design.md` - UI/UX rules for this school operations app.
5. `frontend.md` - frontend architecture and testing conventions.
6. `README.md` - local setup, DB URL, and test commands.

## Current Build Direction

- Complete tasks in `todo.md` in phase order unless the user explicitly asks for
  a different priority.
- Phase 0 is complete.
- Phase 1 is mostly complete; the local PostgreSQL database exists at:
  `postgresql+psycopg://admin:secret@localhost:5432/trial_student_db`.
- Next major work should continue into persistence models, migrations, and
  replacing demo/in-memory auth/referral behavior with database-backed logic.

## Backend Notes

- Backend lives in `backend/`.
- Use `uv sync` and `uv run ...`.
- Use FastAPI, SQLAlchemy, Alembic, Pydantic, and Pydantic Settings.
- FastAPI entrypoint: `backend/app/main.py`.
- API router: `backend/app/api/v1/router.py`.
- Config: `backend/app/core/config.py`.
- Env file location: `backend/app/core/.env`.
- `DB_URL` should include the SQLAlchemy psycopg driver name:
  `postgresql+psycopg://admin:secret@localhost:5432/trial_student_db`.
- Auth context is decoded in `backend/app/middleware/auth.py` and stored on
  `request.state.current_user`; route dependencies in
  `backend/app/permissions/dependencies.py` still enforce authentication, roles,
  and CSRF checks.

## Frontend Notes

- Frontend lives in `frontend/`.
- Follow `design.md` and `frontend.md` before adding screens.
- Prefer route-level data loading/action patterns for new routed screens.
- Keep local component state only for UI-only interactions.
- Temporary `// @ts-nocheck` is acceptable in route modules until route type
  generation is wired.

## Verification

Run these before handing work back when relevant:

```bash
cd backend
uv run pytest

cd ../frontend
npm test
npm run build
```

## Guardrails

- Do not skip ahead in `todo.md` without updating it.
- Update docs when architecture or workflow decisions change.
- Keep the MVP role workflow aligned with `plan.md`.
- Preserve role-based visibility and edit permissions as first-class behavior.
