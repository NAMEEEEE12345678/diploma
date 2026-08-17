import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { getFavorites, removeFavorite } from "../api/favorites";

export default function FavoritesPage() {
  const { token } = useAuth();
  const [items, setItems] = useState([]), [loading, setLoading] = useState(true), [error, setError] = useState(""), [removingId, setRemovingId] = useState(null);
  useEffect(() => { let active = true; getFavorites(token).then((data) => active && setItems(data)).catch((requestError) => active && setError(requestError.message)).finally(() => active && setLoading(false)); return () => { active = false; }; }, [token]);
  async function remove(favorite) { if (removingId) return; setRemovingId(favorite.place_id); setError(""); try { await removeFavorite(token, favorite.place_id); setItems((current) => current.filter((item) => item.place_id !== favorite.place_id)); } catch (requestError) { setError(requestError.message); } finally { setRemovingId(null); } }
  return <section className="section page trips-page favorites-page"><div className="container"><div className="section-heading"><div><p className="eyebrow">Сохранённые места</p><h1 className="page-title">Избранное</h1></div><Link className="button button--coral" to="/destinations">Открыть каталог</Link></div>{error && <p className="catalog-error">{error}</p>}{loading ? <div className="catalog-loading">Загружаем избранное…</div> : !items.length ? <div className="empty-state">Здесь появятся места, которые вы хотите посетить. <Link to="/destinations">Найти место →</Link></div> : <div className="places-grid">{items.map((favorite) => <article className="place-card" key={favorite.id}><img src={favorite.place.image_url} alt={favorite.place.name} /><div className="place-card__body"><span className="pill pill--dark">{favorite.place.category}</span><h3>{favorite.place.name}</h3><p>{favorite.place.description}</p><button className="text-link text-link--danger" onClick={() => remove(favorite)} disabled={removingId !== null}>{removingId === favorite.place_id ? "Удаляем…" : "Убрать из избранного"}</button><Link className="text-link" to="/builder">Создать путешествие →</Link></div></article>)}</div>}</div></section>;
}
