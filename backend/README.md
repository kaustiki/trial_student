# Backend Guide

Short map for understanding the Student Care Referral System backend.

## Big Picture

```txt
Browser / Frontend
        |
        v
FastAPI routes
        |
        v
Services
        |
        v
SQLAlchemy models
        |
        v
PostgreSQL database
```

Main files:

- [app/main.py](app/main.py): creates the FastAPI app and adds middleware/routes.
- [app/api/v1/router.py](app/api/v1/router.py): connects route groups.
- [app/api/v1/routes_auth.py](app/api/v1/routes_auth.py): login/session routes.
- [app/api/v1/routes_referrals.py](app/api/v1/routes_referrals.py): referral workflow routes.
- [app/services/auth.py](app/services/auth.py): auth business logic.
- [app/services/referrals.py](app/services/referrals.py): referral business logic.
- [app/models/referral.py](app/models/referral.py): database table models.
- [app/database/session.py](app/database/session.py): database connection/session setup.

## Request Flow

```txt
Request enters app
        |
        v
Middleware:
"Who is this user, if any?"
Stores result on request.state.current_user
        |
        v
Route dependency:
"Must this route have a user?"
get_current_user checks request.state.current_user
        |
        v
Role dependency:
"Is this user allowed here?"
require_roles checks current_user.role
        |
        v
Route function runs
        |
        v
Service reads/writes database
        |
        v
Response goes back to frontend
```

Code references:

- Middleware: [app/middleware/auth.py](app/middleware/auth.py)
- Auth dependencies: [app/permissions/dependencies.py](app/permissions/dependencies.py)
- Routes: [app/api/v1/routes_auth.py](app/api/v1/routes_auth.py), [app/api/v1/routes_referrals.py](app/api/v1/routes_referrals.py)

## Database

Database connection:

```py
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
```

See [app/database/session.py](app/database/session.py).

Table diagram:

```txt
roles
  |
  v
users -------- referrals -------- students
  |               |
  |               +-- referral_teacher_details
  |               +-- counsellor_reviews
  |               +-- special_educator_reviews
  |               +-- vice_principal_reviews
  |               +-- consultant_reviews
  |               +-- audit_logs
  |               +-- notifications
  |               +-- email_notifications
  |
  +-- auth_sessions
```

Tables in [app/models/referral.py](app/models/referral.py):

- `roles`: allowed app roles, like Teacher, Counsellor, Admin.
- `users`: people who log in and perform workflow actions.
- `auth_sessions`: revocable login sessions backed by refresh token hashes.
- `students`: student profile details used in referrals.
- `referrals`: main case record that moves through the workflow.
- `referral_teacher_details`: teacher-submitted details for a referral.
- `counsellor_reviews`: counsellor review section for a referral.
- `special_educator_reviews`: special educator review section.
- `vice_principal_reviews`: vice principal review section.
- `consultant_reviews`: consultant review section.
- `audit_logs`: history of important changes.
- `notifications`: in-app messages for users.
- `email_notifications`: queued email-style notification records.

Important database words:

- Primary key: the table's own id, like `users.id`.
- Foreign key: a link to another table, like `referrals.student_id -> students.id`.
- Relationship: SQLAlchemy's Python shortcut for moving between linked records.

## Routes

Routes are the API doors the frontend calls.

```txt
GET    = read data
POST   = create data or perform an action
PUT    = update existing data
```

Auth routes in [app/api/v1/routes_auth.py](app/api/v1/routes_auth.py):

- `POST /api/v1/auth/login`: check email/password and set auth cookies.
- `POST /api/v1/auth/forgot-password`: create reset token if account exists.
- `POST /api/v1/auth/reset-password`: set a new password.
- `GET /api/v1/auth/me`: return current logged-in user.
- `POST /api/v1/auth/refresh`: refresh auth cookies.
- `POST /api/v1/auth/logout`: clear auth cookies.
- `GET /api/v1/auth/roles`: list app roles.

Referral routes in [app/api/v1/routes_referrals.py](app/api/v1/routes_referrals.py):

- `GET /api/v1/referrals/form-access/{role}`: visible/editable form sections.
- `POST /api/v1/referrals/preview`: preview referral without saving.
- `POST /api/v1/referrals`: create referral.
- `GET /api/v1/referrals`: list referrals visible to current user.
- `GET /api/v1/referrals/dashboard`: dashboard summary.
- `GET /api/v1/referrals/notifications`: user notifications.
- `GET /api/v1/referrals/{id}`: one referral.
- `POST /api/v1/referrals/{id}/submit`: submit draft referral.
- `PUT /api/v1/referrals/{id}/counsellor-review`: update counsellor review.
- `PUT /api/v1/referrals/{id}/special-educator-review`: update special educator review.
- `PUT /api/v1/referrals/{id}/vice-principal-review`: update vice principal review.
- `PUT /api/v1/referrals/{id}/consultant-review`: update consultant review.
- `PUT /api/v1/referrals/{id}/final-decision`: principal/admin final decision.
- `GET /api/v1/referrals/{id}/timeline`: audit/history timeline.

## Dependencies

A dependency is reusable "do this first" code.

```py
db: Session = Depends(get_db)
```

Means:

```txt
Open a database session before the route runs.
Close it after the route finishes.
```

```py
current_user: UserPublic = Depends(get_current_user)
```

Means:

```txt
This route requires a logged-in user.
```

```py
current_user: UserPublic = Depends(require_roles(Role.TEACHER, Role.ADMIN))
```

Means:

```txt
This route requires a logged-in user whose role is Teacher or Admin.
```

Dependency code lives in [app/permissions/dependencies.py](app/permissions/dependencies.py).

## Tokens And Cookies

Beginner version: after login, the browser has three cookies.

```txt
access_token  = "I am this user"
refresh_token = "Give me a new access_token"
csrf_token    = "This action came from our frontend"
```

The database also has one row:

```txt
auth_sessions = "This refresh_token is still allowed"
```

That is the whole idea.

## Simple Auth Flow

### 1. Login

```txt
User sends email/password
        |
        v
Backend checks users table
        |
        v
Backend creates 3 cookies:
access_token, refresh_token, csrf_token
        |
        v
Backend saves refresh_token hash in auth_sessions table
        |
        v
User is logged in
```

Code:

- Login route: [app/api/v1/routes_auth.py](app/api/v1/routes_auth.py)
- Cookie creation: [app/core/security.py](app/core/security.py)
- Session row creation: [app/services/auth.py](app/services/auth.py)

### 2. Normal API Request

Example:

```txt
GET /api/v1/referrals
```

Flow:

```txt
Browser sends access_token cookie automatically
        |
        v
Auth middleware reads access_token
        |
        v
Backend checks token is valid
        |
        v
Backend finds user from token email
        |
        v
Backend puts user on request.state.current_user
        |
        v
Route can now use current_user
```

Code:

- Middleware: [app/middleware/auth.py](app/middleware/auth.py)
- Token decoding: [app/services/auth.py](app/services/auth.py)
- Current user dependency: [app/permissions/dependencies.py](app/permissions/dependencies.py)

### 3. Refresh

This happens when `access_token` expires.

```txt
Browser sends refresh_token cookie
        |
        v
Backend checks refresh_token is valid
        |
        v
Backend checks auth_sessions table
        |
        v
If session row is active:
create new access_token and refresh_token
        |
        v
Old auth_sessions row is revoked
        |
        v
New auth_sessions row is created
```

Why this exists:

```txt
access_token is short-lived for safety.
refresh_token keeps the user from logging in again every hour.
auth_sessions lets us revoke refresh tokens.
```

### 4. Logout

```txt
Browser sends logout request
        |
        v
Backend revokes auth_sessions row
        |
        v
Backend clears cookies
        |
        v
User is logged out
```

### 5. CSRF

CSRF is only for write actions like `POST` and `PUT`.

```txt
Browser sends csrf_token cookie
Frontend also sends same value in X-CSRF-Token header
Backend compares both values
If they match, write request is allowed
```

## JWT Details

JWT tokens are signed strings. The backend can read them, but users cannot edit
them safely because editing breaks the signature.

Created in [app/core/security.py](app/core/security.py):

```py
payload = {
    "sub": subject,
    "role": role.value,
    "type": token_type,
    "exp": expires_at,
    "jti": "...",
}
```

Token fields:

- `sub`: who the token belongs to, currently user email.
- `role`: user's role at login time.
- `type`: `access` or `refresh`.
- `exp`: expiration time.
- `jti`: random token id so every issued token is unique.

Cookies set by login:

- `access_token`: short-lived token used on normal API requests.
- `refresh_token`: longer-lived token used only to get fresh auth cookies.
- `csrf_token`: readable safety token the frontend sends back in a header.

Database session row created by login:

- `auth_sessions.refresh_token_hash`: hashed copy of the refresh token.
- `auth_sessions.user_id`: user who owns the session.
- `auth_sessions.expires_at`: when the refresh session stops working.
- `auth_sessions.revoked_at`: set when logout/rotation invalidates the session.

Cookie code:

- Set cookies: `set_auth_cookies(...)` in [app/core/security.py](app/core/security.py)
- Clear cookies: `clear_auth_cookies(...)` in [app/core/security.py](app/core/security.py)

Why more than one token?

```txt
access_token answers: who are you on normal requests?
refresh_token answers: can this login continue after access expires?
csrf_token answers: did this POST/PUT come from our frontend?
auth_sessions answers: has this refresh token been revoked?
```

## Authorization

Authorization means:

```txt
Are you allowed to do this?
```

Example:

```py
current_user: UserPublic = Depends(require_roles(Role.SPECIAL_EDUCATOR, Role.ADMIN))
```

Means:

```txt
Special Educator: allowed
Admin: allowed
Teacher: blocked with 403 Forbidden
```

Code reference: `require_roles(...)` in [app/permissions/dependencies.py](app/permissions/dependencies.py).

## Quick Mental Model

```txt
Database models define what can be stored.
Routes define what the frontend can ask for.
Services do the actual work.
Middleware prepares request context.
Dependencies protect routes.
Tokens prove login.
Session rows let refresh tokens be revoked.
Roles decide permission.
CSRF protects cookie-based writes.
```
