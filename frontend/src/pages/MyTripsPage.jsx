import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { deleteTrip, getTrips } from "../api/trips";

export default function MyTripsPage() {
  const { token } = useAuth();
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    let active = true;
    getTrips(token).then((data) => active && setTrips(data)).catch((requestError) => active && setError(requestError.message)).finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [token]);

  async function handleDelete(tripId) {
    if (deletingId) return;
    setDeletingId(tripId); setError("");
    try { await deleteTrip(token, tripId); setTrips((current) => current.filter((trip) => trip.id !== tripId)); }
    catch (requestError) { setError(requestError.message); }
    finally { setDeletingId(null); }
  }

  return <section className="section page trips-page"><div className="container">
    <div className="trips-intro"><div><p className="eyebrow">Ваши истории</p><h1 className="page-title">Коллекция<br /><em>путешествий</em></h1><p>Маршруты, к которым хочется возвращаться.</p></div><Link className="button button--coral" to="/builder">+ Новое путешествие</Link></div>
    {error && <p className="catalog-error">{error}</p>}
    {loading ? <div className="catalog-loading">Загружаем путешествия…</div> : !trips.length ? <div className="empty-state">Пока нет путешествий. <Link to="/builder">Создать первое →</Link></div> : <div className="trip-grid">{trips.map((trip) => <article className="trip-card" key={trip.id}>
      <img src={trip.city.image_url} alt={trip.city.name} /><div className="trip-card__body"><span className="status">Сохранено</span><h2>{trip.title}</h2><p>{trip.city.name} · {trip.start_date} — {trip.end_date}</p><div className="trip-card__actions"><Link to={`/builder/${trip.id}`}>Открыть маршрут →</Link><button className="text-link text-link--danger" onClick={() => handleDelete(trip.id)} disabled={deletingId !== null}>{deletingId === trip.id ? "Удаляем…" : "Удалить"}</button></div></div>
    </article>)}</div>}
  </div></section>;
}
