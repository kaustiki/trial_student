import { ClipboardList, LayoutDashboard, LogOut, UserRound } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuthStore } from "../store/authStore";
import { roleLabels } from "../utils/labels";

export function AppLayout() {
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-paper">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-ocean">
              Student Care
            </p>
            <h1 className="text-xl font-semibold text-ink">Referral System</h1>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 text-sm text-slate-600 sm:flex">
              <UserRound className="h-4 w-4" aria-hidden="true" />
              <span>{user ? roleLabels[user.role] : "Guest"}</span>
            </div>
            <button
              type="button"
              onClick={logout}
              className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-slate-300 bg-white text-slate-600 transition hover:border-slate-400 hover:text-ink"
              aria-label="Log out"
              title="Log out"
            >
              <LogOut className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[220px_1fr] lg:px-8">
        <nav className="flex gap-2 lg:flex-col">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium ${
                isActive
                  ? "bg-ocean text-white"
                  : "bg-white text-slate-700 ring-1 ring-slate-200 hover:bg-slate-50"
              }`
            }
          >
            <LayoutDashboard className="h-4 w-4" aria-hidden="true" />
            Dashboard
          </NavLink>
          <NavLink
            to="/referrals/new"
            className={({ isActive }) =>
              `inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium ${
                isActive
                  ? "bg-ocean text-white"
                  : "bg-white text-slate-700 ring-1 ring-slate-200 hover:bg-slate-50"
              }`
            }
          >
            <ClipboardList className="h-4 w-4" aria-hidden="true" />
            Referral
          </NavLink>
        </nav>
        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
