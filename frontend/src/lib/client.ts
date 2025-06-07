import axios from "axios";
import { config } from "./config";

export const apiClient = axios.create({
  // set base url and default headers
  baseURL: config.apiUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  // intercept requests to add token from localStorage
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// if the token has expired or invalid remove it and reload the page(if it exists)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (localStorage.getItem("token")) {
        localStorage.removeItem("token");
        window.location.reload();
      }
    }
    return Promise.reject(error);
  },
);
