import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import { LaunchList } from "./components/LaunchList";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const AppContent = () => {
  const [showRegister, setShowRegister] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("token"),
  );

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleRegisterSuccess = () => {
    setShowRegister(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
  };

  if (isAuthenticated) {
    return <LaunchList onLogout={handleLogout} />;
  }

  return (
    <div>
      {showRegister ? (
        <Register
          onRegisterSuccess={handleRegisterSuccess}
          onLoginClick={() => setShowRegister(false)}
        />
      ) : (
        <Login
          onLoginSuccess={handleLoginSuccess}
          onRegisterClick={() => setShowRegister(true)}
        />
      )}
    </div>
  );
};

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
};
