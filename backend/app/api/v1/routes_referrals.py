from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.permissions.dependencies import get_current_user, require_roles, verify_csrf_token
from app.permissions.roles import ROLE_EDITABLE_SECTIONS, ROLE_VISIBLE_SECTIONS, Role
from app.schemas.auth import UserPublic
from app.schemas.referral import (
    ConsultantReviewUpdate,
    CounsellorReviewUpdate,
    DashboardSummary,
    FinalDecisionUpdate,
    NotificationPublic,
    ReferralCreate,
    ReferralListItem,
    ReferralPublic,
    ReferralSubmit,
    ReferralTimelineItem,
    RoleFormAccess,
    SpecialEducatorReviewUpdate,
    VicePrincipalReviewUpdate,
)
from app.services.referrals import (
    build_referral_preview,
    create_referral,
    finalize_referral,
    get_dashboard_summary,
    get_timeline,
    list_notifications,
    list_referrals,
    load_referral,
    referral_to_public,
    submit_draft,
    update_review,
)


router = APIRouter()


# GET /api/v1/referrals/form-access/{role}: tell the frontend what a role can see/edit.
@router.get("/form-access/{role}", response_model=RoleFormAccess)
def get_form_access(
    role: Role,
    current_user: UserPublic = Depends(get_current_user),
) -> RoleFormAccess:
    if current_user.role != Role.ADMIN and role != current_user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view form access for your own role",
        )

    return RoleFormAccess(
        role=role,
        visible_sections=sorted(ROLE_VISIBLE_SECTIONS[role]),
        editable_sections=sorted(ROLE_EDITABLE_SECTIONS[role]),
    )


# POST /api/v1/referrals/preview: build a referral response without saving it.
@router.post(
    "/preview",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def preview_referral(
    payload: ReferralCreate,
    current_user: UserPublic = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
) -> ReferralPublic:
    return build_referral_preview(payload)


# POST /api/v1/referrals: create and save a new referral.
@router.post(
    "",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def create_referral_route(
    payload: ReferralCreate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
) -> ReferralPublic:
    return create_referral(db, payload, current_user)


# GET /api/v1/referrals: list referrals visible to the current user.
@router.get("", response_model=list[ReferralListItem])
def list_referrals_route(
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
) -> list[ReferralListItem]:
    return list_referrals(db, current_user)


# GET /api/v1/referrals/dashboard: return counts and dashboard summary data.
@router.get("/dashboard", response_model=DashboardSummary)
def dashboard_route(
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
) -> DashboardSummary:
    return get_dashboard_summary(db, current_user)


# GET /api/v1/referrals/notifications: return unread/read messages for this user.
@router.get("/notifications", response_model=list[NotificationPublic])
def notifications_route(
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
) -> list[NotificationPublic]:
    return list_notifications(db, current_user)


# GET /api/v1/referrals/{referral_id}: load one referral by database id.
@router.get("/{referral_id}", response_model=ReferralPublic)
def get_referral_route(
    referral_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
) -> ReferralPublic:
    return referral_to_public(load_referral(db, referral_id))


# POST /api/v1/referrals/{referral_id}/submit: move a draft referral forward.
@router.post(
    "/{referral_id}/submit",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def submit_referral_route(
    referral_id: int,
    payload: ReferralSubmit,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.TEACHER, Role.ADMIN)),
) -> ReferralPublic:
    if not payload.submit:
        return referral_to_public(load_referral(db, referral_id))
    return submit_draft(db, referral_id, current_user)


# PUT /api/v1/referrals/{referral_id}/counsellor-review: update counsellor fields.
@router.put(
    "/{referral_id}/counsellor-review",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def update_counsellor_review_route(
    referral_id: int,
    payload: CounsellorReviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.STUDENT_COUNSELLOR, Role.ADMIN)),
) -> ReferralPublic:
    return update_review(db, referral_id, current_user, "counsellor_review", payload)


# PUT /api/v1/referrals/{referral_id}/special-educator-review: update special educator fields.
@router.put(
    "/{referral_id}/special-educator-review",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def update_special_educator_review_route(
    referral_id: int,
    payload: SpecialEducatorReviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.SPECIAL_EDUCATOR, Role.ADMIN)),
) -> ReferralPublic:
    # The string tells the shared update_review service which review table/relationship to update.
    return update_review(db, referral_id, current_user, "special_educator_review", payload)


# PUT /api/v1/referrals/{referral_id}/vice-principal-review: update vice principal fields.
@router.put(
    "/{referral_id}/vice-principal-review",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def update_vice_principal_review_route(
    referral_id: int,
    payload: VicePrincipalReviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.VICE_PRINCIPAL, Role.ADMIN)),
) -> ReferralPublic:
    return update_review(db, referral_id, current_user, "vice_principal_review", payload)


# PUT /api/v1/referrals/{referral_id}/consultant-review: update consultant fields.
@router.put(
    "/{referral_id}/consultant-review",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def update_consultant_review_route(
    referral_id: int,
    payload: ConsultantReviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.CONSULTANT, Role.ADMIN)),
) -> ReferralPublic:
    return update_review(db, referral_id, current_user, "consultant_review", payload)


# PUT /api/v1/referrals/{referral_id}/final-decision: close or decide a referral.
@router.put(
    "/{referral_id}/final-decision",
    response_model=ReferralPublic,
    dependencies=[Depends(verify_csrf_token)],
)
def finalize_referral_route(
    referral_id: int,
    payload: FinalDecisionUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(require_roles(Role.PRINCIPAL, Role.ADMIN)),
) -> ReferralPublic:
    return finalize_referral(db, referral_id, current_user, payload)


# GET /api/v1/referrals/{referral_id}/timeline: show audit/history events.
@router.get("/{referral_id}/timeline", response_model=list[ReferralTimelineItem])
def timeline_route(
    referral_id: int,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user),
) -> list[ReferralTimelineItem]:
    return get_timeline(db, referral_id, current_user)
