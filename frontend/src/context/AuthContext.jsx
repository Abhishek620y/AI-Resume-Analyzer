import { createContext, useContext, useEffect, useState } from "react";
import * as authService from "@/services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }
    authService
      .getCurrentUser()
      .then(setUser)
      .catch(() => localStorage.removeItem("access_token"))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const { access_token } = await authService.login(email, password);
    localStorage.setItem("access_token", access_token);
    const currentUser = await authService.getCurrentUser();
    setUser(currentUser);
    return currentUser;
  }

  async function register(email, password, role) {
    await authService.register(email, password, role);
    return login(email, password);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
  }

  const value = { user, loading, login, register, logout, isAuthenticated: !!user };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
