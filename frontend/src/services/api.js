/**
 * Central Axios instance for all backend calls.
 *
 * - Base URL comes from VITE_API_URL (see .env.example), defaulting to
 *   the local backend for dev.
 * - The request interceptor attaches the JWT from localStorage to every
 *   call automatically, so individual API functions never touch headers.
 * - The response interceptor redirects to /login on a 401 (expired or
 *   invalid token), so an expired session doesn't silently show broken
 *   pages.
 */
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "https://ai-resume-analyzer-c35a.onrender.com/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
