import { create } from "zustand";

import type { User } from "../types/auth";

type AuthState = {
  user: User | null;
  setSession: (user: User) => void;
  logout: () => void;
};

const storedUser = localStorage.getItem("scr_user");

export const useAuthStore = create<AuthState>((set) => ({
  user: storedUser ? (JSON.parse(storedUser) as User) : null,
  setSession: (user) => {
    localStorage.setItem("scr_user", JSON.stringify(user));
    set({ user });
  },
  logout: () => {
    localStorage.removeItem("scr_user");
    set({ user: null });
  }
}));
