import { create } from "zustand";
import { subscribeWithSelector, persist } from "zustand/middleware";

interface AuthUser {
  id:       number;
  email:    string;
  name:     string;
  is_staff: boolean;
}

interface AuthState {
  accessToken: string | null;
  user:        AuthUser | null;
}

interface AuthActions {
  setAccessToken: (token: string) => void;
  setUser:        (user: AuthUser) => void;
  clearAuth:      () => void;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  subscribeWithSelector(
    persist(
      (set) => ({
        accessToken:    null,
        user:           null,
        setAccessToken: (token) => set({ accessToken: token }),
        setUser:        (user) => set({ user }),
        clearAuth:      () => set({ accessToken: null, user: null }),
      }),
      { name: "auth-storage", partialize: (state) => ({ user: state.user }) },
    ),
  ),
);
