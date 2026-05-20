from enum import StrEnum


class Role(StrEnum):
    TEACHER = "teacher"
    STUDENT_COUNSELLOR = "student_counsellor"
    SPECIAL_EDUCATOR = "special_educator"
    VICE_PRINCIPAL = "vice_principal"
    CONSULTANT = "consultant"
    PRINCIPAL = "principal"
    ADMIN = "admin"


ROLE_LABELS: dict[Role, str] = {
    Role.TEACHER: "Teacher",
    Role.STUDENT_COUNSELLOR: "Student Counsellor",
    Role.SPECIAL_EDUCATOR: "Special Educator",
    Role.VICE_PRINCIPAL: "Vice Principal",
    Role.CONSULTANT: "Consultant",
    Role.PRINCIPAL: "Principal",
    Role.ADMIN: "Admin",
}


ROLE_EDITABLE_SECTIONS: dict[Role, set[str]] = {
    Role.TEACHER: {"teacher_details"},
    Role.STUDENT_COUNSELLOR: {"counsellor_review"},
    Role.SPECIAL_EDUCATOR: {"special_educator_review"},
    Role.VICE_PRINCIPAL: {"vice_principal_review"},
    Role.CONSULTANT: {"consultant_review"},
    Role.PRINCIPAL: {"final_decision"},
    Role.ADMIN: {
        "teacher_details",
        "counsellor_review",
        "special_educator_review",
        "vice_principal_review",
        "consultant_review",
        "final_decision",
    },
}


ROLE_VISIBLE_SECTIONS: dict[Role, set[str]] = {
    Role.TEACHER: {"student", "referral", "teacher_details", "final_decision"},
    Role.STUDENT_COUNSELLOR: {
        "student",
        "referral",
        "teacher_details",
        "counsellor_review",
    },
    Role.SPECIAL_EDUCATOR: {
        "student",
        "referral",
        "teacher_details",
        "counsellor_review",
        "special_educator_review",
    },
    Role.VICE_PRINCIPAL: {
        "student",
        "referral",
        "teacher_details",
        "counsellor_review",
        "special_educator_review",
        "vice_principal_review",
    },
    Role.CONSULTANT: {
        "student",
        "referral",
        "teacher_details",
        "counsellor_review",
        "special_educator_review",
        "vice_principal_review",
        "consultant_review",
    },
    Role.PRINCIPAL: {
        "student",
        "referral",
        "teacher_details",
        "counsellor_review",
        "special_educator_review",
        "vice_principal_review",
        "consultant_review",
        "final_decision",
    },
    Role.ADMIN: {
        "student",
        "referral",
        "teacher_details",
        "counsellor_review",
        "special_educator_review",
        "vice_principal_review",
        "consultant_review",
        "final_decision",
    },
}
