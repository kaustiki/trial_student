import axios from "axios";

function readCookie(name: string) {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`))
    ?.split("=")[1];
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1",
  withCredentials: true
});

api.interceptors.request.use((config) => {
  const csrfToken = readCookie("csrf_token");
  if (csrfToken) {
    config.headers["X-CSRF-Token"] = decodeURIComponent(csrfToken);
  }
  return config;
});
