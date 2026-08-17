import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { apiRequest } from "../api/client";
import { useToast } from "../components/ToastProvider";

const groups = [
  { title: "Документы", accent: "sky", icon: "✦", items: ["Паспорт", "Билеты", "Бронь жилья", "Страховка", "Виза, если требуется", "Копии документов"] },
  { title: "Деньги и связь", accent: "violet", icon: "◌", items: ["Банковская карта", "Наличные", "Телефон", "Зарядное устройство", "Power Bank", "Наушники"] },
  { title: "Здоровье и уход", accent: "coral", icon: "✚", items: ["Постоянные лекарства", "Обезболивающее", "Пластыри", "Средства личной гигиены", "Солнцезащитный крем", "Антисептик"] },
  { title: "Одежда", accent: "green", icon: "◒", items: ["Нижнее бельё", "Носки", "Удобная обувь", "Верхняя одежда по погоде", "Одежда для сна", "Сменная одежда"] },
  { title: "Полезные вещи", accent: "amber", icon: "☀", items: ["Зубная щётка", "Расчёска", "Бутылка для воды", "Очки или линзы", "Небольшой рюкзак", "Зонт или дождевик"] },
];

const baseItems = groups.flatMap((group) => group.items.map((title, index) => ({ title, key: `${group.title}-${index}` })));

export default function ChecklistPage() {
  const { token } = useAuth();
  const { showToast } = useToast();
  const [saved, setSaved] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);

  const load = async () => { try { setSaved(await apiRequest("/api/v1/checklist", { token })); } finally { setLoading(false); } };
  useEffect(() => { load(); }, [token]);
  const getBaseItem = (key) => saved.find((item) => item.base_key === key);
  const customItems = useMemo(() => saved.filter((item) => !item.base_key), [saved]);
  const done = baseItems.filter((item) => getBaseItem(item.key)?.checked).length + customItems.filter((item) => item.checked).length;
  const total = baseItems.length + customItems.length;
  const progress = total ? (done / total) * 100 : 0;

  const toggle = async (item, isBase) => {
    if (busy) return;
    setBusy(true);
    try {
      let row = isBase ? getBaseItem(item.key) : item;
      if (!row) row = await apiRequest("/api/v1/checklist", { token, method: "POST", body: JSON.stringify({ base_key: item.key }) });
      const updated = await apiRequest(`/api/v1/checklist/${row.id}`, { token, method: "PUT", body: JSON.stringify({ checked: !row.checked }) });
      setSaved((current) => [...current.filter((savedItem) => savedItem.id !== updated.id), updated]);
    } catch { /* The API client already shows an error toast. */ } finally { setBusy(false); }
  };

  const add = async (event) => {
    event.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle || busy) return;
    setBusy(true);
    try {
      const row = await apiRequest("/api/v1/checklist", { token, method: "POST", body: JSON.stringify({ title: trimmedTitle }) });
      setSaved((current) => [...current, row]);
      setTitle("");
      showToast("Пункт добавлен");
    } catch { /* The API client already shows an error toast. */ } finally { setBusy(false); }
  };

  const remove = async (id) => {
    if (busy) return;
    setBusy(true);
    try {
      await apiRequest(`/api/v1/checklist/${id}`, { token, method: "DELETE" });
      setSaved((current) => current.filter((item) => item.id !== id));
      showToast("Пункт удалён");
    } catch { /* The API client already shows an error toast. */ } finally { setBusy(false); }
  };

  return <section className="section page checklist-page">
    <div className="checklist-atmosphere" aria-hidden="true" />
    <div className="container checklist-container">
      <header className="checklist-hero">
        <p className="eyebrow eyebrow--light">Подготовка к путешествию</p>
        <h1>Собирайтесь спокойно.<br /><em>Главное уже под контролем.</em></h1>
        <p className="checklist-hero__copy">Подготовка к дороге — это забота о себе и уверенность, что важное не останется дома.</p>
        <div className="checklist-progress-card">
          <div className="checklist-progress-card__top"><strong>{done} из {total} готово</strong><span>{Math.round(progress)}%</span></div>
          <div className="checklist-progress" aria-label={`Готово ${done} из ${total}`}><i style={{ width: `${progress}%` }} /></div>
        </div>
      </header>

      {loading ? <div className="catalog-loading">Загружаем чек-лист…</div> : <>
        <section className="checklist-add" aria-label="Добавить свой пункт">
          <div><p className="eyebrow">Своя подготовка</p><h2>Добавить своё</h2></div>
          <form onSubmit={add}>
            <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Например, фотоаппарат" maxLength="180" />
            <button className="button button--coral" disabled={busy || !title.trim()}>Добавить</button>
          </form>
        </section>

        <div className="checklist-grid">
          {groups.map((group) => <ChecklistGroup key={group.title} group={group}>
            {group.items.map((itemTitle, index) => {
              const item = { title: itemTitle, key: `${group.title}-${index}` };
              return <ChecklistRow key={item.key} item={item} checked={Boolean(getBaseItem(item.key)?.checked)} busy={busy} onToggle={() => toggle(item, true)} />;
            })}
          </ChecklistGroup>)}
          {customItems.length > 0 && <ChecklistGroup group={{ title: "Мои вещи", accent: "rose", icon: "♥" }}>
            {customItems.map((item) => <ChecklistRow key={item.id} item={item} checked={item.checked} busy={busy} onToggle={() => toggle(item, false)} onRemove={() => remove(item.id)} />)}
          </ChecklistGroup>}
        </div>
      </>}
    </div>
  </section>;
}

function ChecklistGroup({ group, children }) {
  return <section className={`checklist-group checklist-group--${group.accent}`}>
    <h2><span className="checklist-group__icon" aria-hidden="true">{group.icon}</span>{group.title}</h2>
    <div className="checklist-group__items">{children}</div>
  </section>;
}

function ChecklistRow({ item, checked, busy, onToggle, onRemove }) {
  return <label className={`check-item${checked ? " check-item--checked" : ""}`}>
    <input type="checkbox" checked={checked} onChange={onToggle} disabled={busy} />
    <span className="check-item__title">{item.title}</span>
    {onRemove && <button className="check-item__delete" type="button" onClick={(event) => { event.preventDefault(); onRemove(); }} disabled={busy} aria-label={`Удалить «${item.title}»`}>×</button>}
  </label>;
}
