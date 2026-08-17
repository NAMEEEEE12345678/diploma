import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return <main className="not-found"><p className="eyebrow">404</p><h1>Эта точка на карте не найдена.</h1><Link className="button button--dark" to="/">На главную</Link></main>;
}
