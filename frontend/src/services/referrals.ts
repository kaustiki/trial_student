import { api } from "./api";
import type {
  Referral,
  ReferralCreate,
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
