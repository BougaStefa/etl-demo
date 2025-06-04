import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../lib/client";
import type { Launch } from "../types";

export const useLaunches = () => {
  return useQuery<Launch[]>({
    queryKey: ["launches"],
    queryFn: async () => {
      const { data } = await apiClient.get<Launch[]>("/launches/");
      return data;
    },
  });
};
