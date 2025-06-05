import { useMutation } from "@tanstack/react-query";
import { apiClient } from "../lib/client";

type RegisterCredentials = {
  username: string;
  password: string;
  email?: string;
};

type RegisterResponse = {
  message: string;
};

type RegisterError = {
  detail: string;
};

export const useRegister = (onSuccess?: () => void) => {
  return useMutation<RegisterResponse, RegisterError, RegisterCredentials>({
    mutationFn: async (credentials) => {
      const response = await apiClient.post<RegisterResponse>(
        "/register",
        credentials,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      return response.data;
    },
    onSuccess: () => {
      onSuccess?.();
    },
  });
};
