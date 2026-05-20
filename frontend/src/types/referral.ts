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
  created_at: string;
  updated_at: string;
};

export type RoleFormAccess = {
  role: string;
  visible_sections: string[];
  editable_sections: string[];
};
