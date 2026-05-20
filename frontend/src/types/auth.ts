export type Role =
  | "teacher"
  | "student_counsellor"
  | "special_educator"
  | "vice_principal"
  | "consultant"
  | "principal"
  | "admin";

export type User = {
  id: number;
  name: string;
  email: string;
  role: Role;
  is_active: boolean;
};

export type TokenResponse = {
  access_token: string;
  token_type: "bearer";
  user: User;
};
