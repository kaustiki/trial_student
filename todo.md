# Student Care Referral System - Development Todo

## Current Status

- Phase 0 is complete.
- Phase 1 project setup is complete.
- Backend uses FastAPI, SQLAlchemy, Alembic, Pydantic, Pydantic Settings, uv, and PostgreSQL.
- Frontend uses React, Vite, TailwindCSS, React Router, Axios, Zustand, React Hook Form, and Vitest.
- Local DB URL: `postgresql+psycopg://admin:secret@localhost:5432/trial_student_db`.
- Handoff docs exist: `AGENTS.md`, `design.md`, `frontend.md`, `README.md`.
- Phase 3 through Phase 10 MVP work is implemented: persisted models,
  workflow APIs, role-aware forms, dashboards, notifications, case history,
  audit/security hooks, and focused backend/frontend tests.
- Authentication now uses middleware to decode the session cookie into
  `request.state.current_user`, while route dependencies still enforce role and
  CSRF requirements.
- Local PostgreSQL was not reachable during handoff, so run
  `cd backend && uv run alembic upgrade head` after starting the database.

---

## Phase 0 - Planning & Setup

- [x] Finalize project scope
- [x] Confirm workflow between roles
- [x] Finalize user roles
- [x] Finalize referral statuses
- [x] Confirm mandatory vs optional fields
- [x] Define approval hierarchy
- [x] Finalize UI wireframes
- [x] Define school branding requirements
- [x] Decide hosting platform

---

# Phase 1 - Project Setup

## Backend Setup (FastAPI)

- [x] Setup FastAPI project structure
- [x] Document backend stack: FastAPI, SQLAlchemy, Alembic, Pydantic
- [x] Configure virtual environment
- [x] Setup dependency management
- [x] Add uv project configuration
- [x] Setup environment variables
- [x] Store backend URLs in `.env`
- [x] Configure CORS
- [x] Setup API versioning
- [x] Setup logging
- [x] Setup error handling

Recommended Structure:

backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── permissions/
│   ├── database/
│   ├── middleware/
│   └── utils/

---

## Frontend Setup (React)

- [x] Setup React app
- [x] Setup TailwindCSS
- [x] Setup React Router
- [x] Setup state management (Zustand preferred)
- [x] Setup Axios API layer
- [x] Setup protected routes
- [x] Setup reusable form components
- [x] Setup theme/colors

Recommended Structure:

frontend/
├── src/
│   ├── pages/
│   ├── layouts/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   ├── store/
│   ├── routes/
│   ├── utils/
│   └── types/

---

## Database Setup (PostgreSQL)

- [x] Setup PostgreSQL database
- [x] Configure local Docker PostgreSQL URL
- [x] Setup SQLAlchemy
- [x] Setup Alembic migrations
- [x] Create DB connection manager

---

# Phase 2 - Authentication & Authorization

## Authentication

- [x] Create login API
- [x] Create forgot password API
- [x] Create reset password API
- [x] Implement JWT authentication stored in HttpOnly cookies
- [x] Configure SameSite and Secure cookie settings
- [x] Add CSRF protection for state-changing authenticated requests
- [x] Use simple access-token cookie auth for the MVP
- [x] Add logout functionality

---

## User Roles

- [x] Create role enum
- [x] Create permission matrix
- [x] Create role middleware
- [x] Restrict API access by role
- [x] Restrict frontend pages by role

Roles:

- [x] Teacher
- [x] Student Counsellor
- [x] Special Educator
- [x] Vice Principal
- [x] Consultant
- [x] Principal
- [x] Admin

---

# Phase 3 - Database Design

## Create Database Tables

### Users

- [x] users table
- [x] roles table

Fields:
- id
- name
- email
- password_hash
- role_id
- is_active
- created_at

---

### Students

- [x] students table

Fields:
- id
- admission_number
- student_name
- class
- section
- gender
- parent_name
- parent_contact

---

### Referrals

- [x] referrals table

Fields:
- id
- referral_id
- student_id
- teacher_id
- status
- created_at
- updated_at

---

### Teacher Referral Details

- [x] referral_teacher_details table

Fields:
- behavior_issues
- classroom_behavior
- attitude_towards_teachers
- attitude_towards_peers
- previous_teacher_input
- referral_reason
- teacher_notes

---

### Counsellor Review

- [x] counsellor_reviews table

Fields:
- approval_status
- feedback
- parent_response
- intervention_notes
- reviewed_at

---

### Special Educator Review

- [x] special_educator_reviews table

Fields:
- approval_status
- feedback
- recommendation
- reviewed_at

---

### Vice Principal Review

- [x] vice_principal_reviews table

Fields:
- approval_status
- feedback
- reviewed_at

---

### Consultant Review

- [x] consultant_reviews table

Fields:
- approval_status
- feedback
- reviewed_at

---

### Audit Logs

- [x] audit_logs table

Fields:
- id
- user_id
- action
- entity
- previous_value
- updated_value
- timestamp

---

# Phase 4 - Referral Workflow Engine

## Referral Creation

- [x] Create referral form API
- [x] Create draft save functionality
- [x] Submit referral
- [x] Generate referral ID
- [x] Auto timestamp submission

---

## Workflow Progression

- [x] Teacher → Counsellor
- [x] Counsellor → Special Educator
- [x] Special Educator → Vice Principal
- [x] Vice Principal → Consultant
- [x] Consultant → Principal/Admin
- [x] Final closure

---

## Referral Statuses

- [x] Draft
- [x] Submitted
- [x] Pending Review
- [x] Under Review
- [x] Approved
- [x] Rejected
- [x] Escalated
- [x] Closed

---

# Phase 5 - Role-Based Dynamic Forms

## Teacher View

Visible:
- [x] Student details
- [x] Behaviour issues
- [x] Classroom behavior
- [x] Attitude towards teachers
- [x] Attitude towards peers
- [x] Referral reason

Hidden:
- [x] Approval fields
- [x] Counsellor feedback
- [x] Consultant feedback

Editable:
- [x] Teacher fields only

---

## Counsellor View

Visible:
- [x] Teacher inputs
- [x] Counsellor fields

Editable:
- [x] Approval status
- [x] Feedback
- [x] Parent response

---

## Special Educator View

Visible:
- [x] Teacher + Counsellor notes

Editable:
- [x] Special educator fields

---

## Vice Principal View

Visible:
- [x] Full case history

Editable:
- [x] VP approval
- [x] Feedback

---

## Consultant View

Visible:
- [x] Entire student case

Editable:
- [x] Consultant feedback

---

## Admin View

Visible:
- [x] Everything

Editable:
- [x] Everything

---

# Phase 6 - Dashboards

## Teacher Dashboard

- [x] Active referrals
- [x] Pending referrals
- [x] Closed referrals

---

## Counsellor Dashboard

- [x] Assigned referrals
- [x] Pending reviews
- [x] Completed reviews

---

## Principal Dashboard

- [x] School-wide analytics
- [x] Total referrals
- [x] Cases pending
- [x] Referral trends

---

# Phase 7 - Notifications

- [x] In-app notifications
- [x] Email notifications

Triggers:
- [x] Referral submitted
- [x] Review pending
- [x] Feedback added
- [x] Referral closed

---

# Phase 8 - Student Case History

- [x] Timeline view
- [x] Referral history
- [x] Previous interventions
- [x] Parent communication log
- [x] Historical approvals

---

# Phase 9 - Audit & Security

- [x] Audit logs
- [x] Password encryption
- [x] API protection
- [x] Rate limiting
- [x] Activity monitoring
- [x] Session management

---

# Phase 10 - Testing

## Backend Testing

- [x] Add pytest backend test scaffold
- [x] Add initial referral contract tests
- [x] Authentication testing
- [x] Permission testing
- [x] API testing
- [x] Workflow testing

---

## Frontend Testing

- [x] Add frontend test runner
- [x] Add initial component/utility tests
- [x] Form testing
- [x] Role visibility testing
- [x] Responsive testing

---

# Project Instructions

- [x] Add `design.md` with product UI design rules
- [x] Add `frontend.md` with frontend implementation rules
- [x] Add `AGENTS.md` handoff guide for new Codex sessions
- [x] Document preference for React Router client loaders/actions
- [x] Document temporary `// @ts-nocheck` route-module convention
- [x] Add pytest backend test scaffold
- [x] Document SQLAlchemy and Pydantic stack usage

---

## User Acceptance Testing

- [ ] Teacher testing
- [ ] Counsellor testing
- [ ] Principal testing

---

# Phase 11 - Deployment

## Backend

- [ ] Deploy FastAPI server
- [ ] Configure SSL
- [ ] Configure environment variables

---

## Frontend

- [ ] Deploy React app
- [ ] Configure production API URL

---

## Database

- [ ] Setup production PostgreSQL
- [ ] Enable backups

---

# Phase 12 - Future Features

- [ ] Parent portal
- [ ] Student wellbeing score
- [ ] AI behavior insights
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] WhatsApp notifications
- [ ] Appointment booking

---

# MVP Priority (Build First)

1. Authentication
2. Roles & Permissions
3. Referral Form
4. Role-Based Field Visibility
5. Workflow Progression
6. Dashboards
7. Notifications
8. Audit Logs

Goal:
Get an MVP running for one school before scaling.
