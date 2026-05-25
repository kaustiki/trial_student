import { useEffect, useState } from "react";
import { ClipboardCheck, Clock, FileText, Inbox } from "lucide-react";
import { Link } from "react-router-dom";

import { StatusPill } from "../components/StatusPill";
import { getDashboardSummary, getNotifications } from "../services/referrals";
import { useAuthStore } from "../store/authStore";
import type { DashboardSummary, NotificationItem } from "../types/referral";
import { roleLabels, titleize } from "../utils/labels";

const emptySummary: DashboardSummary = {
  active_referrals: 0,
  pending_reviews: 0,
  closed_cases: 0,
  total_referrals: 0,
  recent_referrals: [],
  notifications: 0
};

export function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const [summary, setSummary] = useState<DashboardSummary>(emptySummary);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(() => setSummary(emptySummary));
    getNotifications().then(setNotifications).catch(() => setNotifications([]));
  }, []);

  const metrics = [
    { label: "Active referrals", value: summary.active_referrals, icon: FileText },
    { label: "Pending reviews", value: summary.pending_reviews, icon: Clock },
    { label: "Closed cases", value: summary.closed_cases, icon: ClipboardCheck }
  ];

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <p className="text-sm font-medium text-slate-500">
          {user ? roleLabels[user.role] : "User"} workspace
        </p>
        <h2 className="mt-1 text-2xl font-semibold text-ink">
          Referral workflow dashboard
        </h2>
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

      <section className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <div className="rounded-lg border border-slate-200 bg-white p-5">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-ink">Recent referrals</h3>
            <span className="text-sm text-slate-500">{summary.total_referrals} total</span>
          </div>
          <div className="mt-4 overflow-hidden rounded-md border border-slate-200">
            {summary.recent_referrals.length ? (
              summary.recent_referrals.map((referral) => (
                <Link
                  key={referral.id}
                  to={`/referrals/${referral.id}`}
                  className="grid gap-2 border-b border-slate-200 px-4 py-3 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-[1fr_auto]"
                >
                  <div>
                    <p className="font-semibold text-ink">
                      {referral.student_name} · {referral.referral_id}
                    </p>
                    <p className="text-slate-500">
                      {referral.admission_number} · {referral.teacher_name}
                    </p>
                  </div>
                  <StatusPill status={referral.status} />
                </Link>
              ))
            ) : (
              <p className="px-4 py-6 text-sm text-slate-500">No referrals yet.</p>
            )}
          </div>
        </div>

        <aside className="rounded-lg border border-slate-200 bg-white p-5">
          <div className="flex items-center gap-2">
            <Inbox className="h-4 w-4 text-ocean" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">Notifications</h3>
          </div>
          <div className="mt-4 space-y-3">
            {notifications.length ? (
              notifications.slice(0, 4).map((notification) => (
                <div key={notification.id} className="rounded-md bg-slate-50 p-3 text-sm">
                  <p className="font-medium text-ink">{titleize(notification.trigger)}</p>
                  <p className="mt-1 text-slate-600">{notification.message}</p>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500">No pending notifications.</p>
            )}
          </div>
        </aside>
      </section>
    </div>
  );
}
