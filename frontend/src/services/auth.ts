import { api } from "./api";
import type { TokenResponse } from "../types/auth";

export async function login(email: string, password: string) {
  const { data } = await api.post<TokenResponse>("/auth/login", {
    email,
    password
  });
  return data;
}
