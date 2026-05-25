from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.referral import (
    AuditLog,
    ConsultantReview,
    CounsellorReview,
    EmailNotification,
    FinalOutcome,
    Notification,
    Referral,
    ReferralStatus,
    ReferralTeacherDetails,
    ReviewApprovalStatus,
    RoleModel,
    SpecialEducatorReview,
    Student,
    User,
    VicePrincipalReview,
)
from app.permissions.roles import Role
from app.schemas.auth import UserPublic
from app.schemas.referral import (
    ConsultantReview as ConsultantReviewSchema,
    ConsultantReviewUpdate,
    CounsellorReview as CounsellorReviewSchema,
    CounsellorReviewUpdate,
    DashboardSummary,
    FinalDecision,
    FinalDecisionUpdate,
    NotificationPublic,
    ReferralCreate,
    ReferralListItem,
    ReferralPublic,
    ReferralTimelineItem,
    SpecialEducatorReview as SpecialEducatorReviewSchema,
    SpecialEducatorReviewUpdate,
    StudentBase,
    TeacherReferralDetails,
    VicePrincipalReview as VicePrincipalReviewSchema,
    VicePrincipalReviewUpdate,
)


REVIEW_MODEL_BY_SECTION = {
    "counsellor_review": CounsellorReview,
    "special_educator_review": SpecialEducatorReview,
    "vice_principal_review": VicePrincipalReview,
    "consultant_review": ConsultantReview,
}


NEXT_PENDING_BY_SECTION = {
    "counsellor_review": Role.SPECIAL_EDUCATOR,
    "special_educator_review": Role.VICE_PRINCIPAL,
    "vice_principal_review": Role.CONSULTANT,
    "consultant_review": Role.PRINCIPAL,
}


def get_referral_query():
    return (
        select(Referral)
        .options(
            joinedload(Referral.student),
            joinedload(Referral.teacher).joinedload(User.role),
            joinedload(Referral.teacher_details),
            joinedload(Referral.counsellor_review),
            joinedload(Referral.special_educator_review),
            joinedload(Referral.vice_principal_review),
            joinedload(Referral.consultant_review),
        )
        .order_by(Referral.updated_at.desc())
    )


def build_referral_preview(payload: ReferralCreate, next_id: int = 1) -> ReferralPublic:
    now = datetime.now(UTC)
    status = ReferralStatus.DRAFT if payload.save_as_draft else ReferralStatus.SUBMITTED

    return ReferralPublic(
        id=next_id,
        referral_id=f"SCR-{now:%Y%m%d}-{next_id:04d}",
        status=status,
        student=payload.student,
        teacher_details=payload.teacher_details,
        created_at=now,
        updated_at=now,
        submitted_at=None if payload.save_as_draft else now,
    )


def create_referral(db: Session, payload: ReferralCreate, current_user: UserPublic) -> ReferralPublic:
    user = db.get(User, current_user.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    student = db.scalar(
        select(Student).where(Student.admission_number == payload.student.admission_number)
    )
    student_values = payload.student.model_dump(by_alias=False)
    if student is None:
        student = Student(**student_values)
        db.add(student)
    else:
        for key, value in student_values.items():
            setattr(student, key, value)

    now = datetime.now(UTC)
    status_value = ReferralStatus.DRAFT if payload.save_as_draft else ReferralStatus.SUBMITTED
    referral = Referral(
        referral_id=generate_referral_id(db, now),
        student=student,
        teacher=user,
        status=status_value,
        submitted_at=None if payload.save_as_draft else now,
    )
    db.add(referral)
    db.flush()

    db.add(ReferralTeacherDetails(referral=referral, **payload.teacher_details.model_dump()))
    record_event(
        db,
        current_user,
        referral,
        "created",
        "referral",
        None,
        f"{referral.referral_id}:{status_value.value}",
    )
    if not payload.save_as_draft:
        notify_role(db, Role.STUDENT_COUNSELLOR, referral, "referral_submitted")
    db.commit()
    db.refresh(referral)
    return referral_to_public(load_referral(db, referral.id))


def generate_referral_id(db: Session, now: datetime) -> str:
    count = db.scalar(select(func.count(Referral.id))) or 0
    return f"SCR-{now:%Y%m%d}-{count + 1:04d}"


def load_referral(db: Session, referral_id: int) -> Referral:
    referral = db.scalar(get_referral_query().where(Referral.id == referral_id))
    if referral is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referral not found")
    return referral


def list_referrals(db: Session, current_user: UserPublic) -> list[ReferralListItem]:
    query = get_referral_query()
    if current_user.role == Role.TEACHER:
        query = query.where(Referral.teacher_id == current_user.id)
    return [referral_to_item(referral) for referral in db.scalars(query).unique().all()]


def referral_to_item(referral: Referral) -> ReferralListItem:
    return ReferralListItem(
        id=referral.id,
        referral_id=referral.referral_id,
        status=referral.status,
        student_name=referral.student.student_name,
        admission_number=referral.student.admission_number,
        teacher_name=referral.teacher.name,
        created_at=referral.created_at,
        updated_at=referral.updated_at,
    )


def referral_to_public(referral: Referral) -> ReferralPublic:
    final_decision = None
    if referral.final_outcome or referral.administrative_notes or referral.closed_at:
        final_decision = FinalDecision(
            outcome=referral.final_outcome,
            administrative_notes=referral.administrative_notes,
            closed_at=referral.closed_at,
        )

    return ReferralPublic(
        id=referral.id,
        referral_id=referral.referral_id,
        status=referral.status,
        student=StudentBase.model_validate(referral.student, from_attributes=True),
        teacher_details=TeacherReferralDetails.model_validate(
            referral.teacher_details,
            from_attributes=True,
        ),
        counsellor_review=review_to_schema(referral.counsellor_review, CounsellorReviewSchema),
        special_educator_review=review_to_schema(
            referral.special_educator_review,
            SpecialEducatorReviewSchema,
        ),
        vice_principal_review=review_to_schema(
            referral.vice_principal_review,
            VicePrincipalReviewSchema,
        ),
        consultant_review=review_to_schema(referral.consultant_review, ConsultantReviewSchema),
        final_decision=final_decision,
        submitted_at=referral.submitted_at,
        created_at=referral.created_at,
        updated_at=referral.updated_at,
    )


def review_to_schema(review: Any, schema_type: type) -> Any:
    if review is None:
        return None
    return schema_type.model_validate(review, from_attributes=True)


def submit_draft(db: Session, referral_id: int, current_user: UserPublic) -> ReferralPublic:
    referral = load_referral(db, referral_id)
    if current_user.role not in {Role.ADMIN, Role.TEACHER} or (
        current_user.role == Role.TEACHER and referral.teacher_id != current_user.id
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot submit referral")
    if referral.status != ReferralStatus.DRAFT:
        return referral_to_public(referral)

    referral.status = ReferralStatus.SUBMITTED
    referral.submitted_at = datetime.now(UTC)
    record_event(db, current_user, referral, "submitted", "referral", "draft", "submitted")
    notify_role(db, Role.STUDENT_COUNSELLOR, referral, "referral_submitted")
    db.commit()
    return referral_to_public(load_referral(db, referral.id))


def update_review(
    db: Session,
    referral_id: int,
    current_user: UserPublic,
    section: str,
    payload: (
        CounsellorReviewUpdate
        | SpecialEducatorReviewUpdate
        | VicePrincipalReviewUpdate
        | ConsultantReviewUpdate
    ),
) -> ReferralPublic:
    referral = load_referral(db, referral_id)
    review_model = REVIEW_MODEL_BY_SECTION[section]
    review = getattr(referral, section)
    previous = review.approval_status.value if review else None
    if review is None:
        review = review_model(referral=referral)
        db.add(review)

    for key, value in payload.model_dump().items():
        setattr(review, key, value)
    review.reviewed_at = datetime.now(UTC)
    referral.status = status_after_review(payload.approval_status, section)

    record_event(
        db,
        current_user,
        referral,
        "reviewed",
        section,
        previous,
        payload.approval_status.value,
    )
    if payload.approval_status == ReviewApprovalStatus.APPROVED:
        notify_role(db, NEXT_PENDING_BY_SECTION[section], referral, "review_pending")
    elif payload.approval_status == ReviewApprovalStatus.REJECTED:
        notify_role(db, Role.PRINCIPAL, referral, "review_rejected")
    else:
        notify_role(db, current_user.role, referral, "feedback_added")
    db.commit()
    return referral_to_public(load_referral(db, referral.id))


def status_after_review(approval_status: ReviewApprovalStatus, section: str) -> ReferralStatus:
    if approval_status == ReviewApprovalStatus.REJECTED:
        return ReferralStatus.REJECTED
    if section == "consultant_review" and approval_status == ReviewApprovalStatus.APPROVED:
        return ReferralStatus.APPROVED
    return ReferralStatus.UNDER_REVIEW


def finalize_referral(
    db: Session,
    referral_id: int,
    current_user: UserPublic,
    payload: FinalDecisionUpdate,
) -> ReferralPublic:
    referral = load_referral(db, referral_id)
    previous = referral.final_outcome.value if referral.final_outcome else None
    referral.final_outcome = payload.outcome
    referral.administrative_notes = payload.administrative_notes
    if payload.close_referral:
        referral.status = ReferralStatus.CLOSED
        referral.closed_at = datetime.now(UTC)

    record_event(
        db,
        current_user,
        referral,
        "finalized",
        "final_decision",
        previous,
        payload.outcome.value,
    )
    notify_role(db, Role.TEACHER, referral, "referral_closed")
    db.commit()
    return referral_to_public(load_referral(db, referral.id))


def get_dashboard_summary(db: Session, current_user: UserPublic) -> DashboardSummary:
    referrals = list_referrals(db, current_user)
    pending_statuses = {
        ReferralStatus.SUBMITTED,
        ReferralStatus.PENDING_REVIEW,
        ReferralStatus.UNDER_REVIEW,
        ReferralStatus.ESCALATED,
    }
    notifications = db.scalar(
        select(func.count(Notification.id)).where(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False),
        )
    )
    return DashboardSummary(
        active_referrals=sum(item.status != ReferralStatus.CLOSED for item in referrals),
        pending_reviews=sum(item.status in pending_statuses for item in referrals),
        closed_cases=sum(item.status == ReferralStatus.CLOSED for item in referrals),
        total_referrals=len(referrals),
        recent_referrals=referrals[:5],
        notifications=notifications or 0,
    )


def get_timeline(db: Session, referral_id: int, current_user: UserPublic) -> list[ReferralTimelineItem]:
    referral = load_referral(db, referral_id)
    logs = db.scalars(
        select(AuditLog)
        .where(AuditLog.referral_id == referral.id)
        .order_by(AuditLog.timestamp.asc())
    ).all()
    return [
        ReferralTimelineItem(
            timestamp=log.timestamp,
            action=log.action,
            entity=log.entity,
            detail=log.updated_value,
        )
        for log in logs
    ]


def list_notifications(db: Session, current_user: UserPublic) -> list[NotificationPublic]:
    notifications = db.scalars(
        select(Notification)
        .options(joinedload(Notification.referral))
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    ).all()
    return [
        NotificationPublic(
            id=notification.id,
            referral_id=notification.referral.referral_id if notification.referral else None,
            trigger=notification.trigger,
            message=notification.message,
            is_read=notification.is_read,
            created_at=notification.created_at,
        )
        for notification in notifications
    ]


def record_event(
    db: Session,
    current_user: UserPublic,
    referral: Referral,
    action: str,
    entity: str,
    previous_value: str | None,
    updated_value: str | None,
) -> None:
    db.add(
        AuditLog(
            user_id=current_user.id,
            referral=referral,
            action=action,
            entity=entity,
            previous_value=previous_value,
            updated_value=updated_value,
        )
    )


def notify_role(db: Session, role: Role, referral: Referral, trigger: str) -> None:
    users = db.scalars(select(User).join(RoleModel).where(RoleModel.name == role)).all()
    for user in users:
        message = f"{referral.referral_id} requires {role.value.replace('_', ' ')} attention."
        db.add(
            Notification(
                user_id=user.id,
                referral=referral,
                trigger=trigger,
                message=message,
            )
        )
        db.add(
            EmailNotification(
                user_id=user.id,
                referral_id=referral.id,
                recipient_email=user.email,
                subject=f"Student Care referral update: {referral.referral_id}",
                body=message,
            )
        )
