from fastapi.testclient import TestClient

from app.main import app
from app.permissions.roles import Role
from app.schemas.referral import ReferralCreate
from app.services.referrals import build_referral_preview


client = TestClient(app)


def test_health_check_reports_ok() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_teacher_form_access_is_limited_to_teacher_details() -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"},
    )
    response = client.get(f"/api/v1/referrals/form-access/{Role.TEACHER}")

    assert login_response.status_code == 200
    assert response.status_code == 200
    assert response.json()["role"] == Role.TEACHER
    assert response.json()["editable_sections"] == ["teacher_details"]
    assert "consultant_review" not in response.json()["visible_sections"]


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


def test_preview_referral_requires_teacher_or_admin_role() -> None:
    client.post(
        "/api/v1/auth/login",
        json={"email": "counsellor@example.com", "password": "password"},
    )
    csrf_token = client.cookies.get("csrf_token")

    response = client.post(
        "/api/v1/referrals/preview",
        headers={"X-CSRF-Token": csrf_token or ""},
        json={
            "student": {
                "admission_number": "A001",
                "student_name": "Test Student",
                "class": "5",
            },
            "teacher_details": {
                "behavior_issues": "Frequent disruptions",
                "referral_reason": "Needs care team review",
            },
            "save_as_draft": False,
        },
    )

    assert response.status_code == 403


def test_teacher_can_create_submitted_referral_with_audit_timeline() -> None:
    client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"},
    )
    csrf_token = client.cookies.get("csrf_token")

    create_response = client.post(
        "/api/v1/referrals",
        headers={"X-CSRF-Token": csrf_token or ""},
        json={
            "student": {
                "admission_number": "A002",
                "student_name": "Persisted Student",
                "class": "6",
            },
            "teacher_details": {
                "behavior_issues": "Repeated conflict in class",
                "referral_reason": "Needs structured review",
            },
            "save_as_draft": False,
        },
    )

    assert create_response.status_code == 200
    referral = create_response.json()
    assert referral["status"] == "submitted"
    assert referral["submitted_at"] is not None

    timeline_response = client.get(f"/api/v1/referrals/{referral['id']}/timeline")

    assert timeline_response.status_code == 200
    assert timeline_response.json()[0]["action"] == "created"


def test_counsellor_review_moves_referral_under_review() -> None:
    client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"},
    )
    csrf_token = client.cookies.get("csrf_token")
    referral = client.post(
        "/api/v1/referrals",
        headers={"X-CSRF-Token": csrf_token or ""},
        json={
            "student": {
                "admission_number": "A003",
                "student_name": "Review Student",
                "class": "6",
            },
            "teacher_details": {
                "behavior_issues": "Withdrawal from peer groups",
                "referral_reason": "Needs counsellor review",
            },
            "save_as_draft": False,
        },
    ).json()

    client.post(
        "/api/v1/auth/login",
        json={"email": "counsellor@example.com", "password": "password"},
    )
    csrf_token = client.cookies.get("csrf_token")
    review_response = client.put(
        f"/api/v1/referrals/{referral['id']}/counsellor-review",
        headers={"X-CSRF-Token": csrf_token or ""},
        json={
            "approval_status": "approved",
            "feedback": "Initial counselling complete",
            "parent_response": "Parent informed",
            "intervention_notes": "Weekly check-in",
        },
    )

    assert review_response.status_code == 200
    assert review_response.json()["status"] == "under_review"
    assert review_response.json()["counsellor_review"]["approval_status"] == "approved"
