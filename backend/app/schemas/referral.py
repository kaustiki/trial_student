from datetime import datetime

from pydantic import BaseModel, Field

from app.models.referral import FinalOutcome, ReferralStatus
from app.permissions.roles import Role


class StudentBase(BaseModel):
    admission_number: str
    student_name: str
    class_name: str = Field(alias="class")
    section: str | None = None
    gender: str | None = None
    parent_name: str | None = None
    parent_contact: str | None = None


class TeacherReferralDetails(BaseModel):
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


class ReviewSection(BaseModel):
    approval_status: str | None = None
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
    created_at: datetime
    updated_at: datetime


class RoleFormAccess(BaseModel):
    role: Role
    visible_sections: list[str]
    editable_sections: list[str]
