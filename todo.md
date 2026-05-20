# Student Care Referral System - Development Todo

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

- [ ] Setup PostgreSQL database
- [x] Configure local Docker PostgreSQL URL
- [x] Setup SQLAlchemy
- [x] Setup Alembic migrations
- [x] Create DB connection manager

---

# Phase 2 - Authentication & Authorization

## Authentication

- [ ] Create login API
- [ ] Create forgot password API
- [ ] Create reset password API
- [ ] Implement JWT authentication
- [ ] Setup refresh tokens
- [ ] Add logout functionality

---

## User Roles

- [ ] Create role enum
- [ ] Create permission matrix
- [ ] Create role middleware
- [ ] Restrict API access by role
- [ ] Restrict frontend pages by role

Roles:

- [ ] Teacher
- [ ] Student Counsellor
- [ ] Special Educator
- [ ] Vice Principal
- [ ] Consultant
- [ ] Principal
- [ ] Admin

---

# Phase 3 - Database Design

## Create Database Tables

### Users

- [ ] users table
- [ ] roles table

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

- [ ] students table

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

- [ ] referrals table

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

- [ ] referral_teacher_details table

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

- [ ] counsellor_reviews table

Fields:
- approval_status
- feedback
- parent_response
- intervention_notes
- reviewed_at

---

### Special Educator Review

- [ ] special_educator_reviews table

Fields:
- approval_status
- feedback
- recommendation
- reviewed_at

---

### Vice Principal Review

- [ ] vice_principal_reviews table

Fields:
- approval_status
- feedback
- reviewed_at

---

### Consultant Review

- [ ] consultant_reviews table

Fields:
- approval_status
- feedback
- reviewed_at

---

### Audit Logs

- [ ] audit_logs table

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

- [ ] Create referral form API
- [ ] Create draft save functionality
- [ ] Submit referral
- [ ] Generate referral ID
- [ ] Auto timestamp submission

---

## Workflow Progression

- [ ] Teacher → Counsellor
- [ ] Counsellor → Special Educator
- [ ] Special Educator → Vice Principal
- [ ] Vice Principal → Consultant
- [ ] Consultant → Principal/Admin
- [ ] Final closure

---

## Referral Statuses

- [ ] Draft
- [ ] Submitted
- [ ] Pending Review
- [ ] Under Review
- [ ] Approved
- [ ] Rejected
- [ ] Escalated
- [ ] Closed

---

# Phase 5 - Role-Based Dynamic Forms

## Teacher View

Visible:
- [ ] Student details
- [ ] Behaviour issues
- [ ] Classroom behavior
- [ ] Attitude towards teachers
- [ ] Attitude towards peers
- [ ] Referral reason

Hidden:
- [ ] Approval fields
- [ ] Counsellor feedback
- [ ] Consultant feedback

Editable:
- [ ] Teacher fields only

---

## Counsellor View

Visible:
- [ ] Teacher inputs
- [ ] Counsellor fields

Editable:
- [ ] Approval status
- [ ] Feedback
- [ ] Parent response

---

## Special Educator View

Visible:
- [ ] Teacher + Counsellor notes

Editable:
- [ ] Special educator fields

---

## Vice Principal View

Visible:
- [ ] Full case history

Editable:
- [ ] VP approval
- [ ] Feedback

---

## Consultant View

Visible:
- [ ] Entire student case

Editable:
- [ ] Consultant feedback

---

## Admin View

Visible:
- [ ] Everything

Editable:
- [ ] Everything

---

# Phase 6 - Dashboards

## Teacher Dashboard

- [ ] Active referrals
- [ ] Pending referrals
- [ ] Closed referrals

---

## Counsellor Dashboard

- [ ] Assigned referrals
- [ ] Pending reviews
- [ ] Completed reviews

---

## Principal Dashboard

- [ ] School-wide analytics
- [ ] Total referrals
- [ ] Cases pending
- [ ] Referral trends

---

# Phase 7 - Notifications

- [ ] In-app notifications
- [ ] Email notifications

Triggers:
- [ ] Referral submitted
- [ ] Review pending
- [ ] Feedback added
- [ ] Referral closed

---

# Phase 8 - Student Case History

- [ ] Timeline view
- [ ] Referral history
- [ ] Previous interventions
- [ ] Parent communication log
- [ ] Historical approvals

---

# Phase 9 - Audit & Security

- [ ] Audit logs
- [ ] Password encryption
- [ ] API protection
- [ ] Rate limiting
- [ ] Activity monitoring
- [ ] Session management

---

# Phase 10 - Testing

## Backend Testing

- [ ] Authentication testing
- [ ] Permission testing
- [ ] API testing
- [ ] Workflow testing

---

## Frontend Testing

- [x] Add frontend test runner
- [x] Add initial component/utility tests
- [ ] Form testing
- [ ] Role visibility testing
- [ ] Responsive testing

---

# Project Instructions

- [x] Add `design.md` with product UI design rules
- [x] Add `frontend.md` with frontend implementation rules
- [x] Document preference for React Router client loaders/actions
- [x] Document temporary `// @ts-nocheck` route-module convention
- [x] Add pytest backend test scaffold

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
