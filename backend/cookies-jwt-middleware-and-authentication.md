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

The real project uses this same idea, plus extra safety around refresh tokens,
session rows, roles, and CSRF.
