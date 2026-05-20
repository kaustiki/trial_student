from datetime import UTC, datetime

from app.models.referral import ReferralStatus
from app.schemas.referral import ReferralCreate, ReferralPublic


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
    )
