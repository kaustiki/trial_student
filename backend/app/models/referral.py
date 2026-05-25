from enum import StrEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.permissions.roles import Role


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


class ReviewApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(Role, name="role_name"), unique=True, nullable=False)
    label = Column(String(120), nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(160), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    role = relationship("RoleModel", back_populates="users")
    referrals = relationship("Referral", back_populates="teacher")
    auth_sessions = relationship("AuthSessionRecord", back_populates="user")


class AuthSessionRecord(Base):
    __tablename__ = "auth_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    refresh_token_hash = Column(String(64), unique=True, index=True, nullable=False)
    csrf_token = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="auth_sessions")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    admission_number = Column(String(80), unique=True, index=True, nullable=False)
    student_name = Column(String(160), nullable=False)
    class_name = Column("class", String(40), nullable=False)
    section = Column(String(40), nullable=True)
    gender = Column(String(40), nullable=True)
    parent_name = Column(String(160), nullable=True)
    parent_contact = Column(String(80), nullable=True)

    referrals = relationship("Referral", back_populates="student")


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    referral_id = Column(String(40), unique=True, index=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(
        Enum(ReferralStatus, name="referral_status"),
        default=ReferralStatus.DRAFT,
        index=True,
        nullable=False,
    )
    final_outcome = Column(Enum(FinalOutcome, name="final_outcome"), nullable=True)
    administrative_notes = Column(Text, nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student = relationship("Student", back_populates="referrals")
    teacher = relationship("User", back_populates="referrals")
    teacher_details = relationship(
        "ReferralTeacherDetails",
        back_populates="referral",
        cascade="all, delete-orphan",
        uselist=False,
    )
    counsellor_review = relationship(
        "CounsellorReview",
        back_populates="referral",
        cascade="all, delete-orphan",
        uselist=False,
    )
    special_educator_review = relationship(
        "SpecialEducatorReview",
        back_populates="referral",
        cascade="all, delete-orphan",
        uselist=False,
    )
    vice_principal_review = relationship(
        "VicePrincipalReview",
        back_populates="referral",
        cascade="all, delete-orphan",
        uselist=False,
    )
    consultant_review = relationship(
        "ConsultantReview",
        back_populates="referral",
        cascade="all, delete-orphan",
        uselist=False,
    )
    audit_logs = relationship("AuditLog", back_populates="referral")
    notifications = relationship("Notification", back_populates="referral")


class ReferralTeacherDetails(Base):
    __tablename__ = "referral_teacher_details"

    id = Column(Integer, primary_key=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), unique=True, nullable=False)
    behavior_issues = Column(Text, nullable=False)
    classroom_behavior = Column(Text, nullable=True)
    attitude_towards_teachers = Column(Text, nullable=True)
    attitude_towards_peers = Column(Text, nullable=True)
    previous_teacher_input = Column(Text, nullable=True)
    referral_reason = Column(Text, nullable=False)
    teacher_notes = Column(Text, nullable=True)

    referral = relationship("Referral", back_populates="teacher_details")


class ReviewMixin:
    id = Column(Integer, primary_key=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), unique=True, nullable=False)
    approval_status = Column(
        Enum(ReviewApprovalStatus, name="review_approval_status"),
        default=ReviewApprovalStatus.PENDING,
        nullable=False,
    )
    feedback = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)


class CounsellorReview(ReviewMixin, Base):
    __tablename__ = "counsellor_reviews"

    parent_response = Column(Text, nullable=True)
    intervention_notes = Column(Text, nullable=True)

    referral = relationship("Referral", back_populates="counsellor_review")


class SpecialEducatorReview(ReviewMixin, Base):
    __tablename__ = "special_educator_reviews"

    recommendation = Column(Text, nullable=True)

    referral = relationship("Referral", back_populates="special_educator_review")


class VicePrincipalReview(ReviewMixin, Base):
    __tablename__ = "vice_principal_reviews"

    escalation_comments = Column(Text, nullable=True)

    referral = relationship("Referral", back_populates="vice_principal_review")


class ConsultantReview(ReviewMixin, Base):
    __tablename__ = "consultant_reviews"

    recommendation = Column(Text, nullable=True)

    referral = relationship("Referral", back_populates="consultant_review")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), nullable=True)
    action = Column(String(120), nullable=False)
    entity = Column(String(120), nullable=False)
    previous_value = Column(Text, nullable=True)
    updated_value = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    referral = relationship("Referral", back_populates="audit_logs")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), nullable=True)
    trigger = Column(String(120), nullable=False)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    referral = relationship("Referral", back_populates="notifications")


class EmailNotification(Base):
    __tablename__ = "email_notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), nullable=True)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(40), default="queued", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
