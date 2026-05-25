import { api } from "./api";
import type { AuthSession, ForgotPasswordResponse, MessageResponse } from "../types/auth";

export async function login(email: string, password: string) {
  const { data } = await api.post<AuthSession>("/auth/login", {
    email,
    password
  });
  return data;
}

export async function getCurrentSession() {
  const { data } = await api.get<AuthSession>("/auth/me");
  return data;
}

export async function refreshSession() {
  const { data } = await api.post<AuthSession>("/auth/refresh");
  return data;
}

export async function requestPasswordReset(email: string) {
  const { data } = await api.post<ForgotPasswordResponse>("/auth/forgot-password", {
    email
  });
  return data;
}

export async function resetPassword(token: string, newPassword: string) {
  const { data } = await api.post<MessageResponse>("/auth/reset-password", {
    token,
    new_password: newPassword
  });
  return data;
}

export async function logout() {
  await api.post("/auth/logout");
}
