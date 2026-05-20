from enum import StrEnum


class ReferralStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PENDING_REVIEW = "pending_review"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    CLOSED = "closed"


class FinalOutcome(StrEnum):
    RETAINED = "retained"
    UNDER_OBSERVATION = "under_observation"
    INTERVENTION_REQUIRED = "intervention_required"
    PARENT_COUNSELLING_REQUIRED = "parent_counselling_required"
    EXTERNAL_REFERRAL = "external_referral"
    CLOSED = "closed"
