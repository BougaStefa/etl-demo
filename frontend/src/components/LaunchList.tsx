// src/components/LaunchList.tsx
import { useState } from "react";
import { useLaunches } from "../hooks/useLaunches";
import { useBookmarks, useToggleBookmark } from "../hooks/useBookmarks";
import type { Launch } from "../types";

export const LaunchList = ({ onLogout }: { onLogout: () => void }) => {
  const { data: launches, isLoading, error, refetch } = useLaunches();
  const { data: bookmarks } = useBookmarks();
  const { mutate: toggleBookmark } = useToggleBookmark();
  const [expandedId, setExpandedId] = useState<string | null>(null);

  // set for a faster lookup of bookmarked launches
  const bookmarkedLaunches = new Set(bookmarks?.map((b) => b.launch_id) || []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <p className="text-xl font-medium text-gray-600">
          Loading SpaceX launches...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 gap-4">
        <p className="text-red-600 font-medium">Error loading launches</p>
        <button
          onClick={() => refetch()}
          className="bg-blue-500 text-white px-6 py-2 rounded-lg shadow-sm hover:bg-blue-600 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">SpaceX Launches</h1>
          <div className="flex gap-2">
            <button
              onClick={() => refetch()}
              className="bg-blue-500 text-white px-6 py-2 rounded-lg shadow-sm hover:bg-blue-600 transition-colors"
            >
              Refresh Data
            </button>{" "}
            <button
              onClick={onLogout}
              className="bg-red-500 text-white px-6 py-2 rounded-lg shadow-sm hover:bg-red-600 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {launches?.map((launch: Launch) => (
            <div
              key={launch.id}
              className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {launch.name}
                </h3>
                <button
                  onClick={() => toggleBookmark(launch.id)}
                  className="text-2xl text-yellow-400 hover:text-yellow-500 transition-colors focus:outline-none"
                  aria-label={
                    bookmarkedLaunches.has(launch.id)
                      ? "Remove bookmark"
                      : "Add bookmark"
                  }
                >
                  {bookmarkedLaunches.has(launch.id) ? "★" : "☆"}
                </button>
              </div>
              <p className="text-gray-600 mb-1">
                Flight Number: {launch.flight_number}
              </p>
              <p className="text-gray-600 mb-1">
                Date: {new Date(launch.date_utc).toLocaleDateString()}
              </p>
              <p className="text-gray-600 mb-3">
                Status:{" "}
                {launch.success ? (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium bg-green-100 text-green-800">
                    ✅ Success
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium bg-red-100 text-red-800">
                    ❌ Failure
                  </span>
                )}
              </p>
              <button
                onClick={() =>
                  setExpandedId(expandedId === launch.id ? null : launch.id)
                }
                className="w-full mt-2 bg-gray-100 px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-200 transition-colors"
              >
                {expandedId === launch.id ? "Show Less" : "Show Details"}
              </button>
              {expandedId === launch.id && launch.details && (
                <p className="mt-4 text-gray-600">{launch.details}</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
