import { FormEvent, useState } from "react";
import { LogIn } from "lucide-react";
import { Navigate, useNavigate } from "react-router-dom";

import { Field } from "../components/Field";
import { login } from "../services/auth";
import { useAuthStore } from "../store/authStore";

export function LoginPage() {
  const navigate = useNavigate();
  const { token, setSession } = useAuthStore();
  const [email, setEmail] = useState("teacher@example.com");
  const [password, setPassword] = useState("password");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (token) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      const session = await login(email, password);
      setSession(session.access_token, session.user);
      navigate("/");
    } catch {
      setError("Use a demo account with password: password");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-paper px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
      >
        <p className="text-sm font-semibold uppercase tracking-wide text-ocean">
          Student Care
        </p>
        <h1 className="mt-1 text-2xl font-semibold text-ink">Sign in</h1>
        <p className="mt-2 text-sm text-slate-600">
          Demo accounts: teacher@example.com, counsellor@example.com, admin@example.com.
        </p>

        <div className="mt-6 space-y-4">
          <Field
            label="Email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
          <Field
            label="Password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        {error ? <p className="mt-4 text-sm text-red-600">{error}</p> : null}

        <button
          type="submit"
          disabled={isSubmitting}
          className="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-md bg-ocean px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-cyan-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <LogIn className="h-4 w-4" aria-hidden="true" />
          {isSubmitting ? "Signing in" : "Sign in"}
        </button>
      </form>
    </main>
  );
}
