from app.api.v1.routes_health import health_check
from app.api.v1.routes_referrals import get_form_access
from app.permissions.roles import Role
from app.schemas.referral import ReferralCreate
from app.services.referrals import build_referral_preview


def test_health_check_reports_ok() -> None:
    assert health_check()["status"] == "ok"


def test_teacher_form_access_is_limited_to_teacher_details() -> None:
    access = get_form_access(Role.TEACHER)

    assert access.role == Role.TEACHER
    assert access.editable_sections == ["teacher_details"]
    assert "consultant_review" not in access.visible_sections


def test_submitted_referral_preview_generates_referral_id() -> None:
    payload = ReferralCreate.model_validate(
        {
            "student": {
                "admission_number": "A001",
                "student_name": "Test Student",
                "class": "5",
                "section": "A",
            },
            "teacher_details": {
                "behavior_issues": "Frequent disruptions",
                "referral_reason": "Needs care team review",
            },
            "save_as_draft": False,
        }
    )

    referral = build_referral_preview(payload)

    assert referral.referral_id.startswith("SCR-")
    assert referral.status == "submitted"
