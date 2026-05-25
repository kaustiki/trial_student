import { api } from "./api";
import type {
  DashboardSummary,
  NotificationItem,
  Referral,
  ReferralCreate,
  ReferralListItem,
  ReferralTimelineItem,
  RoleFormAccess
} from "../types/referral";
import type { Role } from "../types/auth";

export async function getFormAccess(role: Role) {
  const { data } = await api.get<RoleFormAccess>(`/referrals/form-access/${role}`);
  return data;
}

export async function previewReferral(payload: ReferralCreate) {
  const { data } = await api.post<Referral>("/referrals/preview", payload);
  return data;
}

export async function createReferral(payload: ReferralCreate) {
  const { data } = await api.post<Referral>("/referrals", payload);
  return data;
}

export async function listReferrals() {
  const { data } = await api.get<ReferralListItem[]>("/referrals");
  return data;
}

export async function getDashboardSummary() {
  const { data } = await api.get<DashboardSummary>("/referrals/dashboard");
  return data;
}

export async function getReferral(id: string | number) {
  const { data } = await api.get<Referral>(`/referrals/${id}`);
  return data;
}

export async function getReferralTimeline(id: string | number) {
  const { data } = await api.get<ReferralTimelineItem[]>(`/referrals/${id}/timeline`);
  return data;
}

export async function getNotifications() {
  const { data } = await api.get<NotificationItem[]>("/referrals/notifications");
  return data;
}

export async function updateReview(id: string | number, section: string, payload: Record<string, string>) {
  const routeBySection: Record<string, string> = {
    counsellor_review: "counsellor-review",
    special_educator_review: "special-educator-review",
    vice_principal_review: "vice-principal-review",
    consultant_review: "consultant-review"
  };
  const { data } = await api.put<Referral>(`/referrals/${id}/${routeBySection[section]}`, payload);
  return data;
}

export async function finalizeReferral(id: string | number, payload: Record<string, string | boolean>) {
  const { data } = await api.put<Referral>(`/referrals/${id}/final-decision`, payload);
  return data;
}
