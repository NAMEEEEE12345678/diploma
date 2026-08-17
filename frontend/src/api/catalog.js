import { apiRequest } from "./client";

export function getCountries() {
  return apiRequest("/api/v1/countries");
}

export function getCities(countryId) {
  const query = countryId ? `?country_id=${countryId}` : "";
  return apiRequest(`/api/v1/cities${query}`);
}

export function getCityPlaces(cityId) {
  return apiRequest(`/api/v1/cities/${cityId}/places`);
}
