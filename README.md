# Student Care Referral System

MVP scaffold for a school referral workflow. The app now includes persisted
users, students, referrals, role reviews, audit logs, notification records, and
role-aware frontend screens for dashboard, referral creation, and case review.

## Backend

Backend stack:

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Pydantic Settings
- PostgreSQL

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Useful endpoints:

- `GET /api/v1/health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/roles`
- `GET /api/v1/referrals/form-access/{role}`
- `POST /api/v1/referrals/preview`
- `POST /api/v1/referrals`
- `GET /api/v1/referrals`
- `GET /api/v1/referrals/dashboard`
- `GET /api/v1/referrals/notifications`
- `GET /api/v1/referrals/{id}`
- `PUT /api/v1/referrals/{id}/counsellor-review`
- `PUT /api/v1/referrals/{id}/special-educator-review`
- `PUT /api/v1/referrals/{id}/vice-principal-review`
- `PUT /api/v1/referrals/{id}/consultant-review`
- `PUT /api/v1/referrals/{id}/final-decision`
- `GET /api/v1/referrals/{id}/timeline`

Login stores auth tokens in cookies:

- `access_token`: short-lived JWT used by normal API requests.
- `refresh_token`: longer-lived JWT used only by `/auth/refresh`.
- `csrf_token`: readable safety token sent back in the `X-CSRF-Token` header.

Refresh tokens are backed by the `auth_sessions` database table, which stores a
hash of the refresh token so sessions can be revoked on logout or token
rotation. Frontend code should send credentials with API requests instead of
reading or storing JWTs manually.

Authentication is split between middleware and route dependencies:

- `AuthContextMiddleware` decodes the `access_token` cookie once per request and
  stores the authenticated user on `request.state.current_user`.
- `get_current_user` reads that request state for protected endpoints.
- `require_roles(...)` stays on individual routes so role access remains visible
  at the endpoint definition.
- CSRF checks remain explicit dependencies on state-changing cookie-auth routes.
- `POST /auth/refresh` checks the `refresh_token` against `auth_sessions`,
  revokes the old row, and creates fresh cookies plus a new session row.

Seed users are created on first auth/database access and use password `password`:

- `teacher@example.com`
- `counsellor@example.com`
- `special@example.com`
- `vp@example.com`
- `consultant@example.com`
- `principal@example.com`
- `admin@example.com`

## Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The frontend expects the backend at `http://localhost:8000/api/v1`.

## Database

Local Docker PostgreSQL:

```bash
docker exec -it tinymagiq-postgres psql -U admin -d trial_student_db
```

The backend reads `DB_URL` from `backend/app/core/.env`:

```env
DB_URL="postgresql+psycopg://admin:secret@localhost:5432/trial_student_db"
```

## Tests

```bash
cd backend
uv run pytest

cd ../frontend
npm test
npm run build
```

## Phase 0 Decisions

- Roles: Teacher, Student Counsellor, Special Educator, Vice Principal,
  Consultant, Principal, Admin.
- Referral statuses: Draft, Submitted, Pending Review, Under Review, Approved,
  Rejected, Escalated, Closed.
- Workflow: Teacher to Counsellor to Special Educator to Vice Principal to
  optional Consultant to Principal/Admin final decision.
- First MVP fields: student details, teacher referral details, role-visible
  review sections, and final decision metadata.
