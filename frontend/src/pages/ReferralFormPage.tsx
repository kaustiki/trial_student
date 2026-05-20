import { useEffect, useState } from "react";
import { Save, Send } from "lucide-react";
import { useForm } from "react-hook-form";

import { Field } from "../components/Field";
import { StatusPill } from "../components/StatusPill";
import { getFormAccess, previewReferral } from "../services/referrals";
import { useAuthStore } from "../store/authStore";
import type { Referral, ReferralCreate, RoleFormAccess } from "../types/referral";
import { titleize } from "../utils/labels";

export function ReferralFormPage() {
  const user = useAuthStore((state) => state.user);
  const [access, setAccess] = useState<RoleFormAccess | null>(null);
  const [preview, setPreview] = useState<Referral | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register, handleSubmit, formState } = useForm<ReferralCreate>({
    defaultValues: {
      save_as_draft: true,
      student: {
        admission_number: "",
        student_name: "",
        class: "",
        section: ""
      },
      teacher_details: {
        behavior_issues: "",
        referral_reason: ""
      }
    }
  });

  useEffect(() => {
    if (!user) return;
    getFormAccess(user.role).then(setAccess).catch(() => setAccess(null));
  }, [user]);

  async function onSubmit(payload: ReferralCreate, submit: boolean) {
    setIsSubmitting(true);
    try {
      const referral = await previewReferral({
        ...payload,
        save_as_draft: !submit
      });
      setPreview(referral);
    } finally {
      setIsSubmitting(false);
    }
  }

  const canEditTeacherFields = access?.editable_sections.includes("teacher_details") ?? false;

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
          <div>
            <p className="text-sm font-medium text-slate-500">New referral</p>
            <h2 className="mt-1 text-2xl font-semibold text-ink">Teacher observation form</h2>
          </div>
          {access ? (
            <div className="rounded-md bg-slate-50 px-3 py-2 text-xs text-slate-600 ring-1 ring-slate-200">
              Editable: {access.editable_sections.map(titleize).join(", ") || "None"}
            </div>
          ) : null}
        </div>
      </section>

      <form
        className="space-y-6"
        onSubmit={handleSubmit((payload) => onSubmit(payload, false))}
      >
        <section className="rounded-lg border border-slate-200 bg-white p-5">
          <h3 className="text-base font-semibold text-ink">Student details</h3>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <Field
              label="Admission number"
              error={formState.errors.student?.admission_number?.message}
              {...register("student.admission_number", { required: "Required" })}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Student name"
              error={formState.errors.student?.student_name?.message}
              {...register("student.student_name", { required: "Required" })}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Class"
              error={formState.errors.student?.class?.message}
              {...register("student.class", { required: "Required" })}
              disabled={!canEditTeacherFields}
            />
            <Field label="Section" {...register("student.section")} disabled={!canEditTeacherFields} />
            <Field label="Gender" {...register("student.gender")} disabled={!canEditTeacherFields} />
            <Field
              label="Parent contact"
              {...register("student.parent_contact")}
              disabled={!canEditTeacherFields}
            />
          </div>
        </section>

        <section className="rounded-lg border border-slate-200 bg-white p-5">
          <h3 className="text-base font-semibold text-ink">Teacher referral details</h3>
          <div className="mt-4 grid gap-4">
            <Field
              label="Behavior issues"
              multiline
              error={formState.errors.teacher_details?.behavior_issues?.message}
              {...register("teacher_details.behavior_issues", { required: "Required" })}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Classroom behavior"
              multiline
              {...register("teacher_details.classroom_behavior")}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Attitude towards teachers"
              {...register("teacher_details.attitude_towards_teachers")}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Attitude towards peers"
              {...register("teacher_details.attitude_towards_peers")}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Previous teacher feedback"
              multiline
              {...register("teacher_details.previous_teacher_input")}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Reason for referral"
              multiline
              error={formState.errors.teacher_details?.referral_reason?.message}
              {...register("teacher_details.referral_reason", { required: "Required" })}
              disabled={!canEditTeacherFields}
            />
            <Field
              label="Supporting comments"
              multiline
              {...register("teacher_details.teacher_notes")}
              disabled={!canEditTeacherFields}
            />
          </div>
        </section>

        <div className="flex flex-col gap-3 sm:flex-row">
          <button
            type="submit"
            disabled={isSubmitting || !canEditTeacherFields}
            className="inline-flex items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Save className="h-4 w-4" aria-hidden="true" />
            Save draft
          </button>
          <button
            type="button"
            disabled={isSubmitting || !canEditTeacherFields}
            onClick={handleSubmit((payload) => onSubmit(payload, true))}
            className="inline-flex items-center justify-center gap-2 rounded-md bg-leaf px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Send className="h-4 w-4" aria-hidden="true" />
            Submit referral
          </button>
        </div>
      </form>

      {preview ? (
        <section className="rounded-lg border border-slate-200 bg-white p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">Generated referral</p>
              <h3 className="text-lg font-semibold text-ink">{preview.referral_id}</h3>
            </div>
            <StatusPill status={preview.status} />
          </div>
        </section>
      ) : null}
    </div>
  );
}
