# Student Care Referral System - Requirements Document

## Functional Requirements

### Authentication

FR-001  
The system shall allow users to login securely.

FR-002  
The system shall support password reset.

FR-003  
The system shall restrict access based on roles.

FR-004  
The system shall maintain user sessions securely.

---

### User Roles & Permissions

FR-005  
The system shall support the following roles:

- Teacher
- Student Counsellor
- Special Educator
- Vice Principal
- Consultant
- Principal
- Admin

FR-006  
The system shall restrict field visibility based on role.

FR-007  
The system shall restrict edit permissions based on role.

FR-008  
The system shall allow Admin to manage users.

---

### Referral Management

FR-009  
Teachers shall be able to create referrals.

FR-010  
Teachers shall be able to save draft referrals.

FR-011  
Teachers shall be able to submit referrals.

FR-012  
Each referral shall have a unique referral ID.

FR-013  
The system shall timestamp every submission.

FR-014  
The system shall allow student search.

---

### Teacher Referral Form

FR-015  
Teacher shall be able to input:

- Behavior issues
- Classroom behavior
- Attitude towards teachers
- Attitude towards peers
- Previous teacher feedback
- Reason for referral
- Supporting comments

FR-016  
Teachers shall not edit approval fields.

---

### Counsellor Review

FR-017  
Counsellor shall review referrals.

FR-018  
Counsellor shall add feedback.

FR-019  
Counsellor shall record parent response.

FR-020  
Counsellor shall approve/reject referral.

---

### Special Educator Review

FR-021  
Special educator shall review referrals.

FR-022  
Special educator shall add observations.

FR-023  
Special educator shall approve/reject referral.

---

### Vice Principal Review

FR-024  
Vice principal shall review referral.

FR-025  
Vice principal shall provide feedback.

FR-026  
Vice principal shall approve/reject referral.

---

### Consultant Review

FR-027  
Consultant shall review case.

FR-028  
Consultant shall add recommendations.

FR-029  
Consultant shall approve/reject referral.

---

### Principal/Admin

FR-030  
Principal/Admin shall finalize referral outcome.

FR-031  
Admin shall assign users and permissions.

FR-032  
Admin shall view analytics.

---

### Referral Statuses

FR-033  
System shall support statuses:

- Draft
- Submitted
- Pending Review
- Under Review
- Approved
- Rejected
- Escalated
- Closed

FR-034  
System shall maintain workflow progression.

---

### Notifications

FR-035  
System shall notify users when action is required.

FR-036  
System shall notify stakeholders on updates.

---

### Student History

FR-037  
System shall maintain complete student referral history.

FR-038  
System shall maintain intervention records.

FR-039  
System shall preserve historical comments.

---

### Audit Logs

FR-040  
System shall log all updates.

FR-041  
System shall record:

- User
- Timestamp
- Action
- Changed values

---

## Non-Functional Requirements

### Security

NFR-001  
Passwords must be encrypted.

NFR-002  
JWT authentication must be implemented.

NFR-003  
APIs must be protected.

NFR-004  
Role-based access control must be enforced.

---

### Performance

NFR-005  
System response time should be below 2 seconds.

NFR-006  
System should support concurrent users.

---

### Reliability

NFR-007  
Automatic backups must be maintained.

NFR-008  
Data consistency must be ensured.

---

### Scalability

NFR-009  
System architecture should support scaling.

---

### Maintainability

NFR-010  
Codebase must be modular.

NFR-011  
API documentation must be maintained.

---

## Recommended Stack

Frontend:
- React
- TailwindCSS
- React Hook Form

Backend:
- FastAPI
- SQLAlchemy
- Alembic

Database:
- PostgreSQL

Authentication:
- JWT

Deployment:
- Vercel
- Railway / Render