import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { getTrips } from "../api/trips";
import { getFavorites } from "../api/favorites";

export default function ProfilePage() {
  const { user, token } = useAuth(); const [stats, setStats] = useState({ trips: null, favorites: null });
  useEffect(() => { let active = true; Promise.all([getTrips(token), getFavorites(token)]).then(([trips, favorites]) => active && setStats({ trips: trips.length, favorites: favorites.length })).catch(() => active && setStats({ trips: 0, favorites: 0 })); return () => { active = false; }; }, [token]);
  return <section className="section page profile-page"><div className="container profile-layout profile-layout--cinematic"><div className="profile-hero"><div><p className="eyebrow eyebrow--light">Личный кабинет</p><h1>Ваше<br /><em>путешествие.</em></h1></div><p>Все идеи, сохранённые места и маршруты — в одной личной коллекции.</p></div><aside className="profile-card"><div className="avatar">{user.full_name.charAt(0).toUpperCase()}</div><p className="profile-card__label">Путешественник</p><h2>{user.full_name}</h2><p>{user.email}</p><nav><a className="profile-nav--active">Профиль</a><Link to="/my-trips">Мои путешествия</Link><Link to="/favorites">Избранные места</Link></nav></aside><div className="profile-content"><p className="eyebrow">Личные данные</p><h2>О вас</h2><div className="profile-details"><div><span>Имя</span><strong>{user.full_name}</strong></div><div><span>Email</span><strong>{user.email}</strong></div></div><div className="profile-stats"><article><span>Маршруты</span><strong>{stats.trips ?? '—'}</strong><Link to="/my-trips">Открыть коллекцию →</Link></article><article><span>Избранные места</span><strong>{stats.favorites ?? '—'}</strong><Link to="/favorites">Смотреть места →</Link></article></div></div></div></section>;
}
