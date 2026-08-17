import { Link } from "react-router-dom";
import { destinations } from "../data/demoData";
import { Reveal, TiltCard } from "../components/VisualEffects";

export default function HomePage() {
 return <div className="experience-home">
  <section className="cinematic-hero">
   <div className="hero-noise"/><div className="hero-sun"/><div className="hero-terrain"/>
   <div className="container cinematic-content"><p className="eyebrow eyebrow--light">Curated travel planner · 2026</p><h1>Путешествие<br/>начинается <em>с идеи.</em></h1><p className="cinematic-lead">Соберите личную историю из городов, вкусов и впечатлений — маршрут останется только вашим.</p>
   <div className="trip-search"><div><small>Направление</small><strong>Куда отправимся?</strong></div><div><small>Когда</small><strong>Выберите даты</strong></div><div><small>Формат</small><strong>В своём ритме</strong></div><Link className="button button--coral" to="/builder">Создать маршрут <span>↗</span></Link></div>
   <div className="hero-scroll"><span/> Листайте, чтобы исследовать</div></div>
  </section>
  <Reveal><section className="section destinations-showcase"><div className="container"><div className="section-heading"><div><p className="eyebrow">Вдохновение</p><h2>Выберите точку<br/><em>на карте</em></h2></div><Link className="text-link" to="/destinations">Все направления →</Link></div><div className="immersive-grid">{destinations.slice(0,3).map((item,index)=><TiltCard key={item.city} className="immersive-card"><img src={item.image} alt={item.city}/><div className="immersive-card__shade"/><span className="card-index">0{index+1}</span><div><p>{item.country}</p><h3>{item.city}</h3><small>{item.tag} · {item.price}</small></div></TiltCard>)}</div></div></section></Reveal>
  <Reveal><section className="journey-story"><div className="container"><p className="eyebrow">Сценарий путешествия</p><h2>От желания —<br/><em>к воспоминанию.</em></h2><div className="story-rail">{[["01","Выберите город","Найдите место, которое откликается."],["02","Соберите впечатления","Добавьте культуру, природу и вкусы."],["03","Получите маршрут","Пусть детали сложатся в ваш ритм."],["04","Отправляйтесь","Всё важное будет под рукой."]].map(([n,t,d])=><article key={n}><span>{n}</span><h3>{t}</h3><p>{d}</p></article>)}</div></div></section></Reveal>
  <Reveal><section className="final-cta"><div className="container"><p className="eyebrow eyebrow--light">Следующая глава</p><h2>Не откладывайте<br/><em>историю.</em></h2><Link to="/builder" className="button button--coral">Начать путешествие <span>→</span></Link></div></section></Reveal>
 </div>
}
