export type ReferralStatus =
  | "draft"
  | "submitted"
  | "pending_review"
  | "under_review"
  | "approved"
  | "rejected"
  | "escalated"
  | "closed";

export type Student = {
  admission_number: string;
  student_name: string;
  class: string;
  section?: string;
  gender?: string;
  parent_name?: string;
  parent_contact?: string;
};

export type TeacherReferralDetails = {
  behavior_issues: string;
  classroom_behavior?: string;
  attitude_towards_teachers?: string;
  attitude_towards_peers?: string;
  previous_teacher_input?: string;
  referral_reason: string;
  teacher_notes?: string;
};

export type ReferralCreate = {
  student: Student;
  teacher_details: TeacherReferralDetails;
  save_as_draft: boolean;
};

export type Referral = ReferralCreate & {
  id: number;
  referral_id: string;
  status: ReferralStatus;
  counsellor_review?: CounsellorReview | null;
  special_educator_review?: SpecialEducatorReview | null;
  vice_principal_review?: VicePrincipalReview | null;
  consultant_review?: ConsultantReview | null;
  final_decision?: FinalDecision | null;
  submitted_at?: string | null;
  created_at: string;
  updated_at: string;
};

export type RoleFormAccess = {
  role: string;
  visible_sections: string[];
  editable_sections: string[];
};

export type ReviewApprovalStatus = "pending" | "approved" | "rejected";

export type ReviewSection = {
  approval_status: ReviewApprovalStatus;
  feedback?: string | null;
  reviewed_at?: string | null;
};

export type CounsellorReview = ReviewSection & {
  parent_response?: string | null;
  intervention_notes?: string | null;
};

export type SpecialEducatorReview = ReviewSection & {
  recommendation?: string | null;
};

export type VicePrincipalReview = ReviewSection & {
  escalation_comments?: string | null;
};

export type ConsultantReview = ReviewSection & {
  recommendation?: string | null;
};

export type FinalDecision = {
  outcome?: string | null;
  administrative_notes?: string | null;
  closed_at?: string | null;
};

export type ReferralListItem = {
  id: number;
  referral_id: string;
  status: ReferralStatus;
  student_name: string;
  admission_number: string;
  teacher_name: string;
  created_at: string;
  updated_at: string;
};

export type DashboardSummary = {
  active_referrals: number;
  pending_reviews: number;
  closed_cases: number;
  total_referrals: number;
  recent_referrals: ReferralListItem[];
  notifications: number;
};

export type ReferralTimelineItem = {
  timestamp: string;
  action: string;
  entity: string;
  detail?: string | null;
};

export type NotificationItem = {
  id: number;
  referral_id?: string | null;
  trigger: string;
  message: string;
  is_read: boolean;
  created_at: string;
};
