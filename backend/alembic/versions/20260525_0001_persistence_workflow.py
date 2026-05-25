"""add persisted workflow tables

Revision ID: 20260525_0001
Revises:
Create Date: 2026-05-25
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260525_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


role_name = sa.Enum(
    "TEACHER",
    "STUDENT_COUNSELLOR",
    "SPECIAL_EDUCATOR",
    "VICE_PRINCIPAL",
    "CONSULTANT",
    "PRINCIPAL",
    "ADMIN",
    name="role_name",
)
referral_status = sa.Enum(
    "DRAFT",
    "SUBMITTED",
    "PENDING_REVIEW",
    "UNDER_REVIEW",
    "APPROVED",
    "REJECTED",
    "ESCALATED",
    "CLOSED",
    name="referral_status",
)
final_outcome = sa.Enum(
    "RETAINED",
    "UNDER_OBSERVATION",
    "INTERVENTION_REQUIRED",
    "PARENT_COUNSELLING_REQUIRED",
    "EXTERNAL_REFERRAL",
    "CLOSED",
    name="final_outcome",
)
review_approval_status = sa.Enum(
    "PENDING",
    "APPROVED",
    "REJECTED",
    name="review_approval_status",
)


def upgrade() -> None:
    role_name.create(op.get_bind(), checkfirst=True)
    referral_status.create(op.get_bind(), checkfirst=True)
    final_outcome.create(op.get_bind(), checkfirst=True)
    review_approval_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", role_name, nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("admission_number", sa.String(length=80), nullable=False),
        sa.Column("student_name", sa.String(length=160), nullable=False),
        sa.Column("class", sa.String(length=40), nullable=False),
        sa.Column("section", sa.String(length=40), nullable=True),
        sa.Column("gender", sa.String(length=40), nullable=True),
        sa.Column("parent_name", sa.String(length=160), nullable=True),
        sa.Column("parent_contact", sa.String(length=80), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_students_admission_number", "students", ["admission_number"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "referrals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("referral_id", sa.String(length=40), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("status", referral_status, nullable=False),
        sa.Column("final_outcome", final_outcome, nullable=True),
        sa.Column("administrative_notes", sa.Text(), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.ForeignKeyConstraint(["teacher_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_referrals_referral_id", "referrals", ["referral_id"], unique=True)
    op.create_index("ix_referrals_status", "referrals", ["status"])
    op.create_table(
        "referral_teacher_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("referral_id", sa.Integer(), nullable=False),
        sa.Column("behavior_issues", sa.Text(), nullable=False),
        sa.Column("classroom_behavior", sa.Text(), nullable=True),
        sa.Column("attitude_towards_teachers", sa.Text(), nullable=True),
        sa.Column("attitude_towards_peers", sa.Text(), nullable=True),
        sa.Column("previous_teacher_input", sa.Text(), nullable=True),
        sa.Column("referral_reason", sa.Text(), nullable=False),
        sa.Column("teacher_notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["referral_id"], ["referrals.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("referral_id"),
    )
    for table_name, extra_columns in (
        ("counsellor_reviews", [sa.Column("parent_response", sa.Text(), nullable=True), sa.Column("intervention_notes", sa.Text(), nullable=True)]),
        ("special_educator_reviews", [sa.Column("recommendation", sa.Text(), nullable=True)]),
        ("vice_principal_reviews", [sa.Column("escalation_comments", sa.Text(), nullable=True)]),
        ("consultant_reviews", [sa.Column("recommendation", sa.Text(), nullable=True)]),
    ):
        op.create_table(
            table_name,
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("referral_id", sa.Integer(), nullable=False),
            sa.Column("approval_status", review_approval_status, nullable=False),
            sa.Column("feedback", sa.Text(), nullable=True),
            sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
            *extra_columns,
            sa.ForeignKeyConstraint(["referral_id"], ["referrals.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("referral_id"),
        )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("referral_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity", sa.String(length=120), nullable=False),
        sa.Column("previous_value", sa.Text(), nullable=True),
        sa.Column("updated_value", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["referral_id"], ["referrals.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("referral_id", sa.Integer(), nullable=True),
        sa.Column("trigger", sa.String(length=120), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["referral_id"], ["referrals.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "email_notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("referral_id", sa.Integer(), nullable=True),
        sa.Column("recipient_email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["referral_id"], ["referrals.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("email_notifications")
    op.drop_table("notifications")
    op.drop_table("audit_logs")
    op.drop_table("consultant_reviews")
    op.drop_table("vice_principal_reviews")
    op.drop_table("special_educator_reviews")
    op.drop_table("counsellor_reviews")
    op.drop_table("referral_teacher_details")
    op.drop_index("ix_referrals_status", table_name="referrals")
    op.drop_index("ix_referrals_referral_id", table_name="referrals")
    op.drop_table("referrals")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_students_admission_number", table_name="students")
    op.drop_table("students")
    op.drop_table("roles")
    review_approval_status.drop(op.get_bind(), checkfirst=True)
    final_outcome.drop(op.get_bind(), checkfirst=True)
    referral_status.drop(op.get_bind(), checkfirst=True)
    role_name.drop(op.get_bind(), checkfirst=True)
