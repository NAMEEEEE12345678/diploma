import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function AuthPage({ mode }) {
  const isLogin = mode === "login";
  const { login, register, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const destination = location.state?.from || "/profile";

  if (isAuthenticated) {
    return <Navigate to={destination} replace />;
  }

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      if (isLogin) {
        await login({ email: form.email, password: form.password });
      } else {
        await register(form);
      }
      navigate(destination, { replace: true });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return <div className="auth-page">
    <Link className="brand auth-brand" to="/"><span className="brand__mark">↗</span><span>маршрут</span></Link>
    <div className="auth-card">
      <p className="eyebrow">Личный кабинет</p>
      <h1>{isLogin ? "С возвращением!" : "Начнём путешествие"}</h1>
      <p className="auth-card__lead">{isLogin ? "Войдите, чтобы продолжить планировать." : "Создайте аккаунт — маршруты будут всегда под рукой."}</p>
      <form onSubmit={handleSubmit}>
        {!isLogin && <label>Ваше имя<input name="full_name" value={form.full_name} onChange={updateField} placeholder="Например, Анна" type="text" required /></label>}
        <label>Email<input name="email" value={form.email} onChange={updateField} placeholder="you@example.com" type="email" required /></label>
        <label>Пароль<input name="password" value={form.password} onChange={updateField} placeholder="Не менее 8 символов" type="password" minLength="8" required /></label>
        {error && <p className="auth-error" role="alert">{error}</p>}
        <button className="button button--coral button--full" disabled={isSubmitting} type="submit">{isSubmitting ? "Подождите…" : isLogin ? "Войти" : "Создать аккаунт"} {!isSubmitting && <span>→</span>}</button>
      </form>
      <p className="auth-switch">{isLogin ? "Ещё нет аккаунта?" : "Уже есть аккаунт?"} <Link to={isLogin ? "/register" : "/login"}>{isLogin ? "Зарегистрироваться" : "Войти"}</Link></p>
    </div>
  </div>;
}
