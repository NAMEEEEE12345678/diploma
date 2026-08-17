import { useEffect, useState } from "react";
import { getCities } from "../api/catalog";
import { getCityWeather } from "../api/weather";

const weatherIcons = {
  clear: "☀",
  cloudy: "☁",
  fog: "〰",
  rain: "☂",
  snow: "❄",
  storm: "ϟ",
};

function iconFor(code) {
  if (code === 0 || code === 1) return weatherIcons.clear;
  if (code === 45 || code === 48) return weatherIcons.fog;
  if (code >= 51 && code <= 67 || code >= 80 && code <= 82) return weatherIcons.rain;
  if (code >= 71 && code <= 77 || code >= 85 && code <= 86) return weatherIcons.snow;
  if (code >= 95) return weatherIcons.storm;
  return weatherIcons.cloudy;
}

function formatTemperature(value) {
  const rounded = Math.round(value);
  return `${rounded > 0 ? "+" : ""}${rounded}°`;
}

function formatDay(value) {
  return new Intl.DateTimeFormat("ru-RU", { weekday: "short", day: "numeric", month: "short" }).format(new Date(`${value}T12:00:00`));
}

export default function WeatherPage() {
  const [cities, setCities] = useState([]);
  const [cityId, setCityId] = useState("");
  const [weather, setWeather] = useState(null);
  const [loadingCities, setLoadingCities] = useState(true);
  const [loadingWeather, setLoadingWeather] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    getCities().then((data) => {
      if (!active) return;
      setCities(data);
      if (data[0]) setCityId(String(data[0].id));
    }).catch(() => active && setError("Не удалось загрузить список городов. Попробуйте позже."))
      .finally(() => active && setLoadingCities(false));
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!cityId) return;
    let active = true;
    setLoadingWeather(true);
    setError("");
    getCityWeather(cityId).then((data) => active && setWeather(data))
      .catch(() => active && setError("Не удалось загрузить погоду. Попробуйте позже."))
      .finally(() => active && setLoadingWeather(false));
    return () => { active = false; };
  }, [cityId]);

  return <section className="section page weather-page">
    <div className="weather-page__glow weather-page__glow--one" aria-hidden="true" />
    <div className="weather-page__glow weather-page__glow--two" aria-hidden="true" />
    <div className="container weather-container">
      <header className="weather-hero">
        <p className="eyebrow eyebrow--light">Погода в путешествии</p>
        <h1>Погода</h1>
        <p>Проверьте погоду перед путешествием и соберите маршрут с комфортом.</p>
        <label className="weather-city-picker"><span>Город</span>
          <select value={cityId} onChange={(event) => setCityId(event.target.value)} disabled={loadingCities}>
            {loadingCities && <option>Загружаем города…</option>}
            {!loadingCities && cities.map((city) => <option key={city.id} value={city.id}>{city.name}</option>)}
          </select>
        </label>
      </header>

      {error && <div className="weather-error" role="alert">{error}</div>}
      {loadingWeather && <WeatherSkeleton />}
      {!loadingWeather && weather && <>
        <article className={`weather-current weather-current--${iconFor(weather.current.weather_code)}`}>
          <div className="weather-current__main"><p className="eyebrow eyebrow--light">Сейчас в {weather.city_name}</p><span className="weather-current__icon" aria-hidden="true">{iconFor(weather.current.weather_code)}</span><strong>{formatTemperature(weather.current.temperature)}C</strong><h2>{weather.current.condition}</h2><p>Ощущается как {formatTemperature(weather.current.apparent_temperature)}C</p></div>
          <dl className="weather-stats"><div><dt>Влажность</dt><dd>{weather.current.humidity}%</dd></div><div><dt>Ветер</dt><dd>{weather.current.wind_speed} м/с</dd></div><div><dt>Минимум</dt><dd>{formatTemperature(weather.current.temperature_min)}C</dd></div><div><dt>Максимум</dt><dd>{formatTemperature(weather.current.temperature_max)}C</dd></div></dl>
        </article>

        <section className="weather-forecast"><div className="weather-forecast__heading"><p className="eyebrow">Ближайшие дни</p><h2>Прогноз</h2></div><div className="weather-forecast__grid">
          {weather.forecast.map((day) => <article className="weather-day" key={day.date}><p>{formatDay(day.date)}</p><span aria-hidden="true">{iconFor(day.weather_code)}</span><strong>{day.condition}</strong><div><b>{formatTemperature(day.temperature_max)}C</b><small>{formatTemperature(day.temperature_min)}C</small></div></article>)}
        </div></section>
      </>}
    </div>
  </section>;
}

function WeatherSkeleton() {
  return <div className="weather-skeleton" aria-label="Загружаем погоду"><div /><div /><div /><div /></div>;
}
