import { useEffect, useMemo, useState } from "react";
import type React from "react";
import { Save } from "lucide-react";
import { useParams } from "react-router-dom";

import { Field } from "../components/Field";
import { StatusPill } from "../components/StatusPill";
import {
  finalizeReferral,
  getFormAccess,
  getReferral,
  getReferralTimeline,
  updateReview
} from "../services/referrals";
import { useAuthStore } from "../store/authStore";
import type { Referral, ReferralTimelineItem, RoleFormAccess } from "../types/referral";
import { titleize } from "../utils/labels";

const reviewSections = [
  { key: "counsellor_review", label: "Counsellor review" },
  { key: "special_educator_review", label: "Special educator review" },
  { key: "vice_principal_review", label: "Vice principal review" },
  { key: "consultant_review", label: "Consultant review" }
];

export function ReferralDetailPage() {
  const { id } = useParams();
  const user = useAuthStore((state) => state.user);
  const [referral, setReferral] = useState<Referral | null>(null);
  const [access, setAccess] = useState<RoleFormAccess | null>(null);
  const [timeline, setTimeline] = useState<ReferralTimelineItem[]>([]);
  const [feedback, setFeedback] = useState("");
  const [approvalStatus, setApprovalStatus] = useState("approved");
  const [extra, setExtra] = useState("");
  const [outcome, setOutcome] = useState("under_observation");

  useEffect(() => {
    if (!id || !user) return;
    getReferral(id).then(setReferral);
    getReferralTimeline(id).then(setTimeline).catch(() => setTimeline([]));
    getFormAccess(user.role).then(setAccess).catch(() => setAccess(null));
  }, [id, user]);

  const editableReviewSection = useMemo(
    () => access?.editable_sections.find((section) => section.endsWith("_review")),
    [access]
  );

  async function handleReviewSubmit() {
    if (!id || !editableReviewSection) return;
    const payload: Record<string, string> = {
      approval_status: approvalStatus,
      feedback
    };
    if (editableReviewSection === "counsellor_review") {
      payload.parent_response = extra;
      payload.intervention_notes = extra;
    } else if (editableReviewSection === "vice_principal_review") {
      payload.escalation_comments = extra;
    } else {
      payload.recommendation = extra;
    }
    const updated = await updateReview(id, editableReviewSection, payload);
    setReferral(updated);
    setTimeline(await getReferralTimeline(id));
  }

  async function handleFinalDecision() {
    if (!id) return;
    const updated = await finalizeReferral(id, {
      outcome,
      administrative_notes: extra,
      close_referral: true
    });
    setReferral(updated);
    setTimeline(await getReferralTimeline(id));
  }

  if (!referral) {
    return <p className="text-sm text-slate-500">Loading referral...</p>;
  }

  const canFinalize = access?.editable_sections.includes("final_decision") ?? false;

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
          <div>
            <p className="text-sm font-medium text-slate-500">{referral.referral_id}</p>
            <h2 className="mt-1 text-2xl font-semibold text-ink">
              {referral.student.student_name}
            </h2>
            <p className="mt-1 text-sm text-slate-600">
              {referral.student.admission_number} · Class {referral.student.class}
              {referral.student.section ? ` ${referral.student.section}` : ""}
            </p>
          </div>
          <StatusPill status={referral.status} />
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <div className="space-y-6">
          <CaseSection title="Teacher referral details">
            <ReadOnly label="Behavior issues" value={referral.teacher_details.behavior_issues} />
            <ReadOnly label="Referral reason" value={referral.teacher_details.referral_reason} />
            <ReadOnly label="Notes" value={referral.teacher_details.teacher_notes} />
          </CaseSection>

          {reviewSections
            .filter((section) => access?.visible_sections.includes(section.key))
            .map((section) => {
              const review = referral[section.key as keyof Referral] as Record<string, string> | null;
              return (
                <CaseSection key={section.key} title={section.label}>
                  <ReadOnly
                    label="Approval"
                    value={review?.approval_status ? titleize(review.approval_status) : "Pending"}
                  />
                  <ReadOnly label="Feedback" value={review?.feedback} />
                  <ReadOnly
                    label="Recommendation"
                    value={review?.recommendation ?? review?.intervention_notes ?? review?.escalation_comments}
                  />
                </CaseSection>
              );
            })}

          {access?.editable_sections.includes(editableReviewSection ?? "") ? (
            <CaseSection title={`Update ${titleize(editableReviewSection ?? "review")}`}>
              <label className="block text-sm font-medium text-slate-700">
                Approval status
                <select
                  value={approvalStatus}
                  onChange={(event) => setApprovalStatus(event.target.value)}
                  className="mt-1 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-ocean focus:ring-2 focus:ring-cyan-100"
                >
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                  <option value="pending">Pending</option>
                </select>
              </label>
              <Field label="Feedback" multiline value={feedback} onChange={(event) => setFeedback(event.target.value)} />
              <Field label="Notes" multiline value={extra} onChange={(event) => setExtra(event.target.value)} />
              <button
                type="button"
                onClick={handleReviewSubmit}
                className="inline-flex items-center gap-2 rounded-md bg-leaf px-4 py-2.5 text-sm font-semibold text-white hover:bg-green-700"
              >
                <Save className="h-4 w-4" aria-hidden="true" />
                Save review
              </button>
            </CaseSection>
          ) : null}

          {canFinalize ? (
            <CaseSection title="Final decision">
              <label className="block text-sm font-medium text-slate-700">
                Outcome
                <select
                  value={outcome}
                  onChange={(event) => setOutcome(event.target.value)}
                  className="mt-1 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-ocean focus:ring-2 focus:ring-cyan-100"
                >
                  <option value="retained">Retained</option>
                  <option value="under_observation">Under observation</option>
                  <option value="intervention_required">Intervention required</option>
                  <option value="parent_counselling_required">Parent counselling required</option>
                  <option value="external_referral">External referral</option>
                  <option value="closed">Closed</option>
                </select>
              </label>
              <Field label="Administrative notes" multiline value={extra} onChange={(event) => setExtra(event.target.value)} />
              <button
                type="button"
                onClick={handleFinalDecision}
                className="inline-flex items-center gap-2 rounded-md bg-ocean px-4 py-2.5 text-sm font-semibold text-white hover:bg-cyan-800"
              >
                <Save className="h-4 w-4" aria-hidden="true" />
                Close case
              </button>
            </CaseSection>
          ) : null}
        </div>

        <aside className="rounded-lg border border-slate-200 bg-white p-5">
          <h3 className="text-base font-semibold text-ink">Case timeline</h3>
          <div className="mt-4 space-y-3">
            {timeline.length ? (
              timeline.map((item) => (
                <div key={`${item.timestamp}-${item.action}`} className="border-l-2 border-cyan-200 pl-3">
                  <p className="text-sm font-medium text-ink">{titleize(item.action)}</p>
                  <p className="text-xs text-slate-500">{titleize(item.entity)}</p>
                  {item.detail ? <p className="mt-1 text-sm text-slate-600">{item.detail}</p> : null}
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500">No timeline entries yet.</p>
            )}
          </div>
        </aside>
      </section>
    </div>
  );
}

function CaseSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-5">
      <h3 className="text-base font-semibold text-ink">{title}</h3>
      {children}
    </section>
  );
}

function ReadOnly({ label, value }: { label: string; value?: string | null }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-1 text-sm text-slate-700">{value || "Not recorded"}</p>
    </div>
  );
}
