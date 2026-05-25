from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.referral import FinalOutcome, ReferralStatus, ReviewApprovalStatus
from app.permissions.roles import Role


class StudentBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    admission_number: str
    student_name: str
    class_name: str = Field(alias="class")
    section: str | None = None
    gender: str | None = None
    parent_name: str | None = None
    parent_contact: str | None = None


class TeacherReferralDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    behavior_issues: str
    classroom_behavior: str | None = None
    attitude_towards_teachers: str | None = None
    attitude_towards_peers: str | None = None
    previous_teacher_input: str | None = None
    referral_reason: str
    teacher_notes: str | None = None


class ReferralCreate(BaseModel):
    student: StudentBase
    teacher_details: TeacherReferralDetails
    save_as_draft: bool = True


class ReferralSubmit(BaseModel):
    submit: bool = True


class ReviewSection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    approval_status: ReviewApprovalStatus = ReviewApprovalStatus.PENDING
    feedback: str | None = None
    reviewed_at: datetime | None = None


class CounsellorReview(ReviewSection):
    parent_response: str | None = None
    intervention_notes: str | None = None


class SpecialEducatorReview(ReviewSection):
    recommendation: str | None = None


class VicePrincipalReview(ReviewSection):
    escalation_comments: str | None = None


class ConsultantReview(ReviewSection):
    recommendation: str | None = None


class FinalDecision(BaseModel):
    outcome: FinalOutcome | None = None
    administrative_notes: str | None = None
    closed_at: datetime | None = None


class ReferralPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    referral_id: str
    status: ReferralStatus
    student: StudentBase
    teacher_details: TeacherReferralDetails
    counsellor_review: CounsellorReview | None = None
    special_educator_review: SpecialEducatorReview | None = None
    vice_principal_review: VicePrincipalReview | None = None
    consultant_review: ConsultantReview | None = None
    final_decision: FinalDecision | None = None
    submitted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class RoleFormAccess(BaseModel):
    role: Role
    visible_sections: list[str]
    editable_sections: list[str]


class ReferralListItem(BaseModel):
    id: int
    referral_id: str
    status: ReferralStatus
    student_name: str
    admission_number: str
    teacher_name: str
    created_at: datetime
    updated_at: datetime


class DashboardSummary(BaseModel):
    active_referrals: int
    pending_reviews: int
    closed_cases: int
    total_referrals: int
    recent_referrals: list[ReferralListItem]
    notifications: int


class ReferralTimelineItem(BaseModel):
    timestamp: datetime
    action: str
    entity: str
    detail: str | None = None


class NotificationPublic(BaseModel):
    id: int
    referral_id: str | None = None
    trigger: str
    message: str
    is_read: bool
    created_at: datetime


class CounsellorReviewUpdate(BaseModel):
    approval_status: ReviewApprovalStatus
    feedback: str | None = None
    parent_response: str | None = None
    intervention_notes: str | None = None


class SpecialEducatorReviewUpdate(BaseModel):
    approval_status: ReviewApprovalStatus
    feedback: str | None = None
    recommendation: str | None = None


class VicePrincipalReviewUpdate(BaseModel):
    approval_status: ReviewApprovalStatus
    feedback: str | None = None
    escalation_comments: str | None = None


class ConsultantReviewUpdate(BaseModel):
    approval_status: ReviewApprovalStatus
    feedback: str | None = None
    recommendation: str | None = None


class FinalDecisionUpdate(BaseModel):
    outcome: FinalOutcome
    administrative_notes: str | None = None
    close_referral: bool = True
