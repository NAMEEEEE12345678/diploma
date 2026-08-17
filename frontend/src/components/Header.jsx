import { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const navigation = [
  { to: "/destinations", label: "Направления" },
  { to: "/builder", label: "Конструктор" },
  { to: "/my-trips", label: "Мои путешествия" },
  { to: "/checklist", label: "Чек-лист" },
  { to: "/weather", label: "Погода" },
];

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const closeMenu = () => setIsOpen(false);

  return (
    <header className="header">
      <div className="container header__content">
        <Link className="brand" to="/" onClick={closeMenu}>
          <span className="brand__mark">↗</span>
          <span>маршрут</span>
        </Link>
        <button className="menu-button" onClick={() => setIsOpen(!isOpen)} aria-label="Открыть меню">
          <span></span><span></span><span></span>
        </button>
        <nav className={isOpen ? "nav nav--open" : "nav"}>
          {navigation.map((item) => (
            <NavLink key={item.to} to={item.to} onClick={closeMenu}>
              {item.label}
            </NavLink>
          ))}
          <NavLink to="/profile" className="nav__profile" onClick={closeMenu}>Профиль</NavLink>
        </nav>
        {user ? (
          <div className="header__account">
            <Link to="/favorites" title="Избранное">♥</Link>
            <Link to="/profile" title="Профиль">{user.full_name.split(" ")[0]}</Link>
            <button onClick={logout}>Выйти</button>
          </div>
        ) : <Link className="header__login" to="/login">Войти</Link>}
      </div>
    </header>
  );
}
