# Cookies, JWT, Middleware, And Authentication

This is the simplest version of the JWT auth flow.

JWT is a signed note.

```txt
Login creates the note.
Cookie stores the note.
Browser sends the note.
Middleware reads the note.
Dependency requires the note.
Route uses the user from the note.
```

## 1. Create Token On Login

A JWT is just a signed string that says:

```txt
This user is teacher@example.com.
This token expires later.
Trust it only if the signature is valid.
```

Example:

```py
from datetime import UTC, datetime, timedelta

from jose import jwt


SECRET_KEY = "my-secret"
ALGORITHM = "HS256"


def create_access_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
```

If login succeeds:

```py
token = create_access_token("teacher@example.com")
```

The token is a string like:

```txt
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

You do not need to understand the string itself.

## 2. Store Token In Cookie

```py
from fastapi import Response


def login(response: Response):
    token = create_access_token("teacher@example.com")

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
    )

    return {"message": "logged in"}
```

Now the browser has:

```txt
access_token=<jwt>
```

Because it is a cookie, the browser sends it automatically on later requests.

## 3. Read Token From Cookie

```py
from fastapi import Request


def read_cookie(request: Request):
    token = request.cookies.get("access_token")
    return token
```

So every request can do:

```py
token = request.cookies.get("access_token")
```

## 4. Decode And Verify Token

```py
from fastapi import HTTPException
from jose import JWTError, jwt


def get_user_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return email
```

This checks:

```txt
Is the signature valid?
Is the token expired?
```

If the token was edited or expired, `jwt.decode(...)` fails.

## 5. Middleware Uses The Token

Middleware runs before the route.

```py
class AuthMiddleware:
    async def dispatch(self, request, call_next):
        request.state.current_user = None

        token = request.cookies.get("access_token")

        if token:
            email = get_user_from_token(token)
            request.state.current_user = email

        response = await call_next(request)
        return response
```

Meaning:

```txt
For every request:
1. Read access_token cookie
2. Decode token
3. Put user email on request.state.current_user
4. Continue to route
```

## 6. Route Requires A User

```py
from fastapi import HTTPException, Request


def get_current_user(request: Request) -> str:
    user = request.state.current_user

    if user is None:
        raise HTTPException(status_code=401, detail="Not logged in")

    return user
```

Then a route can use it:

```py
from fastapi import Depends


@app.get("/me")
def me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}
```

If logged in:

```json
{
  "email": "teacher@example.com"
}
```

If not logged in:

```json
{
  "detail": "Not logged in"
}
```

## Whole Flow

```txt
LOGIN
email/password correct
        |
        v
create JWT with email
        |
        v
store JWT in access_token cookie

REQUEST
browser sends access_token cookie
        |
        v
middleware reads cookie
        |
        v
jwt.decode checks token
        |
        v
email goes into request.state.current_user
        |
        v
dependency checks current_user exists
        |
        v
route runs
```

## Tiny Version

```txt
JWT is a signed note.

Login creates the note.
Cookie stores the note.
Browser sends the note.
Middleware reads the note.
Dependency requires the note.
Route uses the user from the note.
```

## CSRF Token Note

With cookie-based login, the browser sends cookies automatically. That means a
bad website might try to trigger a `POST` or `PUT` request using your existing
login cookie.

The CSRF token protects write requests:

```txt
access_token = proves the user is logged in
csrf_token   = helps prove the request came from our frontend
```

The common pattern is:

```txt
1. Backend creates csrf_token.
2. Backend stores it in a readable cookie.
3. Frontend reads the csrf_token cookie.
4. Frontend sends the same value in the X-CSRF-Token header.
5. Backend allows the request only if cookie value == header value.
```

This is called the double-submit cookie pattern.

Example backend creates the CSRF cookie:

```py
import secrets

from fastapi import Response


def set_login_cookies(response: Response, access_token: str):
    csrf_token = secrets.token_urlsafe(32)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
    )
```

Important difference:

```txt
access_token is HttpOnly, so frontend JavaScript cannot read it.
csrf_token is readable, because frontend must copy it into a header.
```

Example frontend copies cookie into request header:

```ts
function readCookie(name: string) {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`))
    ?.split("=")[1];
}

const csrfToken = readCookie("csrf_token");

if (csrfToken) {
  config.headers["X-CSRF-Token"] = decodeURIComponent(csrfToken);
}
```

Example backend checks cookie and header:

```py
from fastapi import Cookie, Header, HTTPException


def verify_csrf_token(
    csrf_cookie: str | None = Cookie(default=None, alias="csrf_token"),
    csrf_header: str | None = Header(default=None, alias="X-CSRF-Token"),
) -> None:
    if csrf_cookie is None or csrf_header is None or csrf_cookie != csrf_header:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
```

Example route uses the CSRF check:

```py
from fastapi import Depends


@router.post("/referrals", dependencies=[Depends(verify_csrf_token)])
def create_referral():
    return {"message": "referral created"}
```

Flow with values:

```txt
Cookie:
csrf_token=abc123

Header:
X-CSRF-Token: abc123

Result:
allowed
```

Bad request:

```txt
Cookie:
csrf_token=abc123

Header:
missing

Result:
blocked
```

Tiny version:

```txt
Access token proves the user.
CSRF token proves the write request.
```

The real project uses this same JWT cookie idea, plus extra safety around roles
and CSRF.
