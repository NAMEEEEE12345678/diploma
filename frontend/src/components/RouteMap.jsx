import { useEffect, useMemo, useState } from "react";
import { CircleMarker, MapContainer, Popup, Polyline, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const DAY_COLORS = ["#ef9b75", "#76c2cb", "#f2cf75", "#bd9ae5", "#9ac984"];

function MapBounds({ points }) {
  const map = useMap();
  useEffect(() => {
    if (points.length === 1) map.setView(points[0].coordinates, 13);
    if (points.length > 1) map.fitBounds(points.map((point) => point.coordinates), { padding: [38, 38] });
  }, [map, points]);
  return null;
}

export default function RouteMap({ days }) {
  const [activeDay, setActiveDay] = useState("all");
  const routeDays = days.map((day) => ({ ...day, items: day.items.filter((item) => item.place?.latitude != null && item.place?.longitude != null) })).filter((day) => day.items.length);
  const visibleDays = activeDay === "all" ? routeDays : routeDays.filter((day) => day.id === Number(activeDay));
  const points = useMemo(() => visibleDays.flatMap((day, index) => day.items.map((item) => ({
    id: item.id, dayNumber: day.day_number, color: DAY_COLORS[(day.day_number - 1) % DAY_COLORS.length],
    coordinates: [item.place.latitude, item.place.longitude], item,
  }))), [visibleDays]);

  if (!points.length) return <section className="route-map route-map--empty"><div><span>⌁</span><h3>Маршрут появится на карте</h3><p>Добавьте место вручную или составьте маршрут автоматически.</p></div></section>;

  return <section className="route-map">
    <div className="route-map__head"><div><p className="eyebrow">Карта маршрута</p><h3>Ваш путь по городу</h3></div><div className="map-day-switcher"><button className={activeDay === "all" ? "active" : ""} onClick={() => setActiveDay("all")}>Все дни</button>{routeDays.map((day) => <button key={day.id} className={activeDay === day.id ? "active" : ""} onClick={() => setActiveDay(day.id)}>День {day.day_number}</button>)}</div></div>
    <MapContainer className="route-map__canvas" center={points[0].coordinates} zoom={12} scrollWheelZoom={false}>
      <TileLayer attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <MapBounds points={points} />
      {visibleDays.map((day) => <Polyline key={day.id} positions={day.items.map((item) => [item.place.latitude, item.place.longitude])} pathOptions={{ color: DAY_COLORS[(day.day_number - 1) % DAY_COLORS.length], weight: 4, opacity: .75 }} />)}
      {points.map((point) => <CircleMarker key={point.id} center={point.coordinates} radius={11} pathOptions={{ color: "#fff", weight: 3, fillColor: point.color, fillOpacity: 1 }}><Popup><strong>{point.item.place.name}</strong><br />День {point.dayNumber} · {point.item.start_time || "время не задано"}<br /><small>{point.item.place.category}</small></Popup></CircleMarker>)}
    </MapContainer>
  </section>;
}
