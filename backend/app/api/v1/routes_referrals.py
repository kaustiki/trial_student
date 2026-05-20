from fastapi import APIRouter

from app.permissions.roles import ROLE_EDITABLE_SECTIONS, ROLE_VISIBLE_SECTIONS, Role
from app.schemas.referral import ReferralCreate, ReferralPublic, RoleFormAccess
from app.services.referrals import build_referral_preview


router = APIRouter()


@router.get("/form-access/{role}", response_model=RoleFormAccess)
def get_form_access(role: Role) -> RoleFormAccess:
    return RoleFormAccess(
        role=role,
        visible_sections=sorted(ROLE_VISIBLE_SECTIONS[role]),
        editable_sections=sorted(ROLE_EDITABLE_SECTIONS[role]),
    )


@router.post("/preview", response_model=ReferralPublic)
def preview_referral(payload: ReferralCreate) -> ReferralPublic:
    return build_referral_preview(payload)
