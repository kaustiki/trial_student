# Student Care Referral System

MVP scaffold for a school referral workflow. Phase 0 decisions are captured in
the local constants and schemas, while Phase 1 provides a runnable FastAPI API
and React/Tailwind frontend shell.

## Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Useful endpoints:

- `GET /api/v1/health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/roles`
- `GET /api/v1/referrals/form-access/{role}`
- `POST /api/v1/referrals/preview`

Demo users use password `password`:

- `teacher@example.com`
- `counsellor@example.com`
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
docker exec -it tinymagiq-postgres psql -U admin -d postgres
```

The backend reads `DB_URL` from `backend/app/core/.env`:

```env
DB_URL=postgresql+psycopg://admin:secret@localhost:5432/postgres
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
