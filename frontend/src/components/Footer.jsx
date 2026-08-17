import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__content">
        <Link className="brand brand--light" to="/"><span className="brand__mark">↗</span><span>маршрут</span></Link>
        <p>Собирайте путешествия, которые хочется прожить.</p>
        <p className="footer__note">© 2026 Маршрут</p>
      </div>
    </footer>
  );
}
