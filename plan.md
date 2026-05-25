# Student Care Referral System - Project Plan

## Overview

The Student Care Referral System is a web-based platform designed for schools to identify, track, review, and manage students requiring special attention due to behavioral, emotional, academic, or developmental concerns.

Teachers can initiate referrals based on observations. These referrals move through a structured review workflow involving counsellors, special educators, vice principals, consultants, and administrators.

The platform ensures:

- Structured referral tracking
- Role-based visibility and editing
- Secure student case management
- Approval workflow
- Audit trail of decisions and feedback

---

## Problem Statement

Currently, schools often manage student concerns using manual forms, spreadsheets, or fragmented communication.

Challenges include:

- No centralized referral system
- Missing follow-ups
- Lack of visibility into case progress
- Difficulty assigning responsibility
- No role-based access control
- Inconsistent documentation

This system solves these challenges through a centralized workflow-driven platform.

---

## Core Objective

Build a secure role-based referral system where:

1. Teachers identify and refer students needing support.
2. Referrals are reviewed by appropriate stakeholders.
3. Each role can only view/edit relevant fields.
4. Student cases are documented and tracked.
5. Schools gain visibility into student support workflows.

---

## User Roles

### 1. Teacher
Primary initiator of referral.

Responsibilities:
- Create student referral
- Fill behavioral observations
- Submit supporting details

Can Edit:
- Behavior issues
- Classroom behavior
- Attitude towards teachers
- Attitude towards peers
- Previous teacher inputs
- Specific reason for referral
- Initial notes

Can View:
- Status of referral
- Final comments (optional)

Cannot Edit:
- Approval statuses
- Counsellor feedback
- Principal remarks
- Consultant feedback

---

### 2. Student Counsellor

Responsibilities:
- Review referral
- Conduct counselling review
- Engage parents if needed

Can Edit:
- Counsellor approval status
- Counsellor feedback
- Parent response
- Intervention notes

Can View:
- Teacher observations
- Referral history

Cannot Edit:
- Teacher inputs
- Principal decisions

---

### 3. Special Educator

Responsibilities:
- Assess special learning or behavioral requirements

Can Edit:
- Special educator approval status
- Special educator feedback
- Recommendations

Can View:
- Teacher observations
- Counsellor notes

Cannot Edit:
- Previous role inputs

---

### 4. Vice Principal

Responsibilities:
- Academic oversight
- Escalation review

Can Edit:
- Vice principal approval status
- Vice principal feedback
- Escalation comments

Can View:
- Entire referral history

---

### 5. Consultant

Responsibilities:
- External/internal specialist review

Can Edit:
- Consultant approval status
- Consultant feedback

Can View:
- Entire student case

---

### 6. Principal / Admin

Responsibilities:
- Final oversight
- Referral closure

Can Edit:
- Final referral status
- Administrative notes

Can View:
- Entire system

Permissions:
- User management
- Role assignment
- Analytics access

---

## Referral Workflow

Teacher Creates Referral
↓
Student Counsellor Review
↓
Special Educator Review
↓
Vice Principal Review
↓
Consultant Review (Optional)
↓
Principal/Admin Final Decision

Final Status:
- Retained
- Under Observation
- Intervention Required
- Parent Counselling Required
- External Referral
- Closed

---

## Major Modules

### 1. Authentication Module

Features:
- Login
- Forgot password
- Role-based access
- JWT authentication stored in HttpOnly cookies
- SameSite cookie protection, with Secure cookies in production
- CSRF protection for state-changing authenticated requests

---

### 2. User Management

Admin can:
- Create users
- Assign roles
- Reset passwords
- Activate/deactivate accounts

Roles:
- Teacher
- Counsellor
- Special Educator
- Vice Principal
- Consultant
- Principal
- Admin

---

### 3. Referral Management

Teachers can:
- Create referral
- Save draft
- Submit referral

System features:
- Referral ID generation
- Student search
- Auto timestamps
- Status tracking

---

### 4. Role-Based Dynamic Forms

Field visibility changes by role.

Example:

Teacher sees:
✔ Behavior Issues  
✔ Teacher Notes

Teacher does NOT see:
✘ Consultant Feedback

Counsellor sees:
✔ Teacher Notes  
✔ Counsellor Fields

Editable fields depend on role permissions.

---

### 5. Review & Approval Engine

Each role:
- Reviews referral
- Adds comments
- Approves/rejects
- Moves workflow forward

Statuses:
- Pending
- Under Review
- Approved
- Rejected
- Escalated

---

### 6. Student Case History

Single timeline showing:
- Referral creation
- Role feedback
- Parent response
- Approval progression
- Previous interventions

---

### 7. Notifications

Email or in-app notifications:

Examples:
- "New referral assigned"
- "Referral pending review"
- "Feedback added"
- "Referral closed"

---

### 8. Dashboard

Teacher Dashboard:
- Active referrals
- Pending reviews
- Closed referrals

Counsellor Dashboard:
- Assigned referrals

Principal Dashboard:
- School-wide analytics

Metrics:
- Total referrals
- Pending cases
- Most common issues
- Intervention success rate

---

## Suggested Technology Stack

### Frontend
React.js

Recommended:
- React Router
- React Hook Form
- TailwindCSS
- Zustand/Redux Toolkit

---

### Backend
FastAPI

Recommended:
- JWT Authentication stored in HttpOnly cookies
- SQLAlchemy ORM
- Alembic Migrations
- Role Middleware

---

### Database
PostgreSQL

Why:
- Strong relational structure
- Audit logs
- Workflow tracking
- Role permissions

---

### Storage
AWS S3 / Supabase Storage (optional)

For:
- Documents
- Reports
- Referral attachments

---

### Deployment

Frontend:
- Vercel

Backend:
- Railway / Render / AWS

Database:
- PostgreSQL Managed DB

---

## Future Enhancements

### Phase 2
- Parent portal
- Student wellbeing score
- AI-powered behavior insights
- Risk alerts
- Referral analytics

### Phase 3
- Mobile application
- WhatsApp notifications
- Counselor scheduling
- Appointment booking

---

## Security Requirements

- Role-based permissions
- Encrypted passwords
- Audit logging
- Activity history
- Student data privacy
- Secure APIs

---

## Estimated Development Phases

### Phase 1
Authentication + Referral Flow

### Phase 2
Role Permissions + Dashboard

### Phase 3
Notifications + Analytics

### Phase 4
Reports + Optimization
