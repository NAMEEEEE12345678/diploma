import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import DestinationsPage from "./pages/DestinationsPage";
import BuilderPage from "./pages/BuilderPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import MyTripsPage from "./pages/MyTripsPage";
import ProfilePage from "./pages/ProfilePage";
import NotFoundPage from "./pages/NotFoundPage";
import FavoritesPage from "./pages/FavoritesPage";
import ChecklistPage from "./pages/ChecklistPage";
import WeatherPage from "./pages/WeatherPage";
import ProtectedRoute from "./auth/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/destinations" element={<DestinationsPage />} />
        <Route path="/builder" element={<ProtectedRoute><BuilderPage /></ProtectedRoute>} />
        <Route path="/builder/:tripId" element={<ProtectedRoute><BuilderPage /></ProtectedRoute>} />
        <Route path="/my-trips" element={<ProtectedRoute><MyTripsPage /></ProtectedRoute>} />
        <Route path="/favorites" element={<ProtectedRoute><FavoritesPage /></ProtectedRoute>} />
        <Route path="/checklist" element={<ProtectedRoute><ChecklistPage /></ProtectedRoute>} />
        <Route path="/weather" element={<WeatherPage />} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
      </Route>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
