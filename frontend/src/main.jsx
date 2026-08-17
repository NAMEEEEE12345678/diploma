import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./auth/AuthContext";
import { ToastProvider } from "./components/ToastProvider";
import "./styles.css";
import "./cinematic.css";
import "./polish.css";
import "./inner-polish.css";
import "./atmosphere.css";
import "./builder-atmosphere.css";
import "./cinematic-dark.css";
import "./focused-fixes.css";
import "./route-map.css";
import "./favorites.css";
import "./favorites-background.css";
import "./toasts.css";
import "./stabilization.css";
import "./editorial-cards.css";
import "./checklist.css";
import "./weather.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider><App /></ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
