import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LaunchList } from "./components/LaunchList";
import { Login } from "./components/Login";
import { useState, useEffect } from "react";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="app">
        {isAuthenticated ? (
          <LaunchList />
        ) : (
          <Login onLoginSuccess={handleLoginSuccess} />
        )}
      </div>
    </QueryClientProvider>
  );
}

export default App;
