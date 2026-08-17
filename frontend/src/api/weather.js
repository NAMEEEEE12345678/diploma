import { apiRequest } from "./client";

export function getCityWeather(cityId) {
  return apiRequest(`/api/v1/weather?city_id=${encodeURIComponent(cityId)}`);
}
