# Frontend Implementation Notes

## Stack

- React
- React Router
- TailwindCSS
- React Hook Form
- Axios
- Zustand only where app-wide session or shared state is truly needed
- Vitest and Testing Library for frontend tests

## Routing Preference

For new routed screens, prefer route-level data APIs instead of adding local
state for every request:

- Use `clientLoader` for data reads.
- Use `clientAction` for form submissions and mutations.
- Keep component state for temporary UI-only behavior.
- Add `// @ts-nocheck` at the top of route modules when route type generation is
  not wired yet, then remove it once generated route types are available.

## Authentication

- Treat the backend session as cookie-based: the JWT is stored in an HttpOnly
  cookie set by the API, not in `localStorage` or regular JavaScript-readable
  cookies.
- Use `credentials: "include"` for `fetch` or `withCredentials: true` for Axios
  when calling authenticated API endpoints.
- Do not manually read, store, or attach the access token in frontend code.
- Send the readable `csrf_token` cookie value in the `X-CSRF-Token` header for
  state-changing authenticated requests.

## Form Direction

- Use React Hook Form for field registration and validation.
- Keep form components reusable and plain.
- Prefer server/API contracts from `src/types` over ad hoc inline shapes.

## Testing

- Add at least one focused test for each reusable component with important
  formatting or behavior.
- Add utility tests for formatting helpers and permission logic.
- Prefer user-visible assertions with Testing Library.
