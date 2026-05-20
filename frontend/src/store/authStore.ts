import { create } from "zustand";

import type { User } from "../types/auth";

type AuthState = {
  token: string | null;
  user: User | null;
  setSession: (token: string, user: User) => void;
  logout: () => void;
};

const storedToken = localStorage.getItem("scr_token");
const storedUser = localStorage.getItem("scr_user");

export const useAuthStore = create<AuthState>((set) => ({
  token: storedToken,
  user: storedUser ? (JSON.parse(storedUser) as User) : null,
  setSession: (token, user) => {
    localStorage.setItem("scr_token", token);
    localStorage.setItem("scr_user", JSON.stringify(user));
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem("scr_token");
    localStorage.removeItem("scr_user");
    set({ token: null, user: null });
  }
}));
