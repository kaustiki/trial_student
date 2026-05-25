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

export type AuthSession = {
  user: User;
};

export type ForgotPasswordResponse = {
  message: string;
  reset_token?: string | null;
};

export type MessageResponse = {
  message: string;
};
