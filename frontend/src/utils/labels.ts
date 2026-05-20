import type { Role } from "../types/auth";

export const roleLabels: Record<Role, string> = {
  teacher: "Teacher",
  student_counsellor: "Student Counsellor",
  special_educator: "Special Educator",
  vice_principal: "Vice Principal",
  consultant: "Consultant",
  principal: "Principal",
  admin: "Admin"
};

export function titleize(value: string) {
  return value
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
