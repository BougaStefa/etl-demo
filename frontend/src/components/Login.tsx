import { useState } from "react";
import { useAuth } from "../hooks/useAuth";

//!TODO: Add user feedback for failed login attempts
//
// redirects to launches page on successful login
export const Login = ({
  onLoginSuccess,
  onRegisterClick,
}: {
  onLoginSuccess: () => void;
  onRegisterClick: () => void;
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showError, setShowError] = useState(false);
  // custom login hook that handles authentication
  const { mutate: login, isPending } = useAuth(onLoginSuccess, () =>
    setShowError(true),
  ); // renamed to login for clarity

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShowError(false);
    login({ username, password });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            SpaceX Launch Tracker
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Sign in to view launches
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="username" className="sr-only">
                Username
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Username"
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Password"
              />
            </div>
          </div>
          {/* Display error message if login fails */}
          {showError && (
            <div className="text-red-600 text-sm text-center">
              Invalid username or password
            </div>
          )}
          <div>
            <button
              type="submit"
              disabled={isPending}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400"
            >
              {/* Show loading state when signing in */}
              {isPending ? "Signing in..." : "Sign in"}
            </button>
          </div>
          <div className="text-sm text-center mt-4">
            <a
              href="#"
              className="font-medium text-blue-600 hover:text-blue-500"
              onClick={(e) => {
                e.preventDefault();
                onRegisterClick();
              }}
            >
              Don't have an account? Sign up
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};
