const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiRequest(path, options = {}) {
  const { token, successMessage, ...requestOptions } = options;
  const headers = new Headers(options.headers);
  headers.set("Accept", "application/json");

  if (options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response;
  try {
    response = await fetch(`${API_URL}${path}`, { ...requestOptions, headers });
  } catch {
    const message = "Не удалось подключиться к серверу. Попробуйте позже.";
    window.dispatchEvent(new CustomEvent("trip-constructor:toast", { detail: { message, type: "error" } }));
    throw new ApiError(message, 0);
  }

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const message = typeof body?.detail === "string"
      ? body.detail
      : "Не удалось выполнить запрос. Попробуйте ещё раз.";
    if (response.status === 401) {
      window.dispatchEvent(new Event("trip-constructor:unauthorized"));
    }
    window.dispatchEvent(new CustomEvent("trip-constructor:toast", { detail: { message, type: "error" } }));
    throw new ApiError(message, response.status);
  }

  if (successMessage) {
    window.dispatchEvent(new CustomEvent("trip-constructor:toast", { detail: { message: successMessage, type: "success" } }));
  }
  return body;
}
