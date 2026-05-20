import { ClipboardCheck, Clock, FileText } from "lucide-react";

import { useAuthStore } from "../store/authStore";
import { roleLabels } from "../utils/labels";

const metrics = [
  { label: "Active referrals", value: "0", icon: FileText },
  { label: "Pending reviews", value: "0", icon: Clock },
  { label: "Closed cases", value: "0", icon: ClipboardCheck }
];

export function DashboardPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <p className="text-sm font-medium text-slate-500">
          {user ? roleLabels[user.role] : "User"} workspace
        </p>
        <h2 className="mt-1 text-2xl font-semibold text-ink">
          Referral workflow dashboard
        </h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
          Phase 1 establishes the protected shell, role context, and form access model.
          Live referral data and analytics are ready to connect once persistence lands.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <article
              key={metric.label}
              className="rounded-lg border border-slate-200 bg-white p-5"
            >
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-slate-500">{metric.label}</p>
                <Icon className="h-5 w-5 text-leaf" aria-hidden="true" />
              </div>
              <p className="mt-3 text-3xl font-semibold text-ink">{metric.value}</p>
            </article>
          );
        })}
      </section>
    </div>
  );
}
