import { useMutation } from "@tanstack/react-query";
import { apiClient } from "../lib/client";

// Define structure of credentials, api response, and error
type LoginCredentials = {
  username: string;
  password: string;
};

type LoginResponse = {
  access_token: string;
  token_type: string;
};

type LoginError = {
  message: string;
};

// hook handles authentication
export const useAuth = (onSuccess?: () => void) => {
  return useMutation<LoginResponse, LoginError, LoginCredentials>({
    // performs login http request with encoded credentials
    mutationFn: async (credentials) => {
      const response = await apiClient.post<LoginResponse>(
        "/token",
        new URLSearchParams(credentials),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        },
      );
      return response.data;
    },
    onSuccess: (data) => {
      // store token in localStorage
      localStorage.setItem("token", data.access_token);
      // execute if provided
      onSuccess?.();
    },
  });
};
