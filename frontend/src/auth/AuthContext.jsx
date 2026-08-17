import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { getCurrentUser, loginUser, registerUser } from "../api/auth";

const TOKEN_KEY = "trip_constructor_access_token";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => sessionStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    let isActive = true;
    setIsLoading(true);
    getCurrentUser(token)
      .then((currentUser) => isActive && setUser(currentUser))
      .catch(() => {
        sessionStorage.removeItem(TOKEN_KEY);
        isActive && setToken(null);
      })
      .finally(() => isActive && setIsLoading(false));

    return () => { isActive = false; };
  }, [token]);

  async function login(credentials) {
    const response = await loginUser(credentials);
    sessionStorage.setItem(TOKEN_KEY, response.access_token);
    setToken(response.access_token);
    const currentUser = await getCurrentUser(response.access_token);
    setUser(currentUser);
    return currentUser;
  }

  async function register(payload) {
    await registerUser(payload);
    return login({ email: payload.email, password: payload.password });
  }

  function logout() {
    sessionStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  }

  useEffect(() => {
    window.addEventListener("trip-constructor:unauthorized", logout);
    return () => window.removeEventListener("trip-constructor:unauthorized", logout);
  }, []);

  const value = useMemo(() => ({
    user,
    token,
    isLoading,
    isAuthenticated: Boolean(token && user),
    login,
    register,
    logout,
  }), [user, token, isLoading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth должен использоваться внутри AuthProvider.");
  }
  return context;
}
