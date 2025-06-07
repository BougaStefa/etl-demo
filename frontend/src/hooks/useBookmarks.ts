import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../lib/client";

interface Bookmark {
  id: number;
  launch_id: string;
  created_at: string;
}

export const useBookmarks = () => {
  return useQuery<Bookmark[]>({
    queryKey: ["bookmarks"],
    queryFn: async () => {
      const { data } = await apiClient.get<Bookmark[]>("/bookmarks/");
      return data;
    },
  });
};

export const useToggleBookmark = () => {
  const queryClient = useQueryClient();
  const timestamp = new Date().toISOString();

  return useMutation({
    mutationFn: async (launchId: string) => {
      try {
        await apiClient.post("/bookmarks/", { launch_id: launchId });
      } catch (error: any) {
        // If it's a 400 error (duplicate bookmark), delete it instead
        if (error.response?.status === 400) {
          await apiClient.delete(`/bookmarks/${launchId}`);
        } else {
          throw error;
        }
      }
    },

    // optimistic updating workaround to address bookmark icon delayed update
    onMutate: async (launchId) => {
      // cancel queries to prevent race conditions
      await queryClient.cancelQueries({ queryKey: ["bookmarks"] });

      // snapshot the previous values in case we need to rollback
      const previousBookmarks =
        queryClient.getQueryData<Bookmark[]>(["bookmarks"]) || [];

      // optimistically update the bookmarks
      const isCurrentlyBookmarked = previousBookmarks.some(
        (b) => b.launch_id === launchId,
      );

      if (isCurrentlyBookmarked) {
        // remove
        queryClient.setQueryData<Bookmark[]>(["bookmarks"], (old) =>
          (old || []).filter((b) => b.launch_id !== launchId),
        );
      } else {
        // add
        const optimisticBookmark: Bookmark = {
          id: Math.random(), // temporary ID
          launch_id: launchId,
          created_at: timestamp,
        };
        queryClient.setQueryData<Bookmark[]>(["bookmarks"], (old) => [
          ...(old || []),
          optimisticBookmark,
        ]);
      }

      // return the snapshot so we can rollback if something goes wrong
      return { previousBookmarks };
    },
    onError: (_err, _newTodo, context) => {
      // Rollback to the snapshot on error
      if (context?.previousBookmarks) {
        queryClient.setQueryData(["bookmarks"], context.previousBookmarks);
      }
    },
    onSettled: () => {
      // Refetch bookmarks after mutation
      queryClient.invalidateQueries({ queryKey: ["bookmarks"] });
    },
  });
};
