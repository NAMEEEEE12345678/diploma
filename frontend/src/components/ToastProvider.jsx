import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = "success") => {
    if (!message) return;
    const id = `${Date.now()}-${Math.random()}`;
    setToasts((current) => [...current, { id, message, type }]);
    window.setTimeout(() => {
      setToasts((current) => current.filter((toast) => toast.id !== id));
    }, 4200);
  }, []);

  useEffect(() => {
    const handleToast = (event) => {
      showToast(event.detail?.message, event.detail?.type);
    };
    window.addEventListener("trip-constructor:toast", handleToast);
    return () => window.removeEventListener("trip-constructor:toast", handleToast);
  }, [showToast]);

  const value = useMemo(() => ({ showToast }), [showToast]);
  return <ToastContext.Provider value={value}>
    {children}
    <div className="toast-stack" aria-live="polite" aria-atomic="true">
      {toasts.map((toast) => <div className={`toast toast--${toast.type}`} key={toast.id} role="status">
        <span>{toast.type === "error" ? "!" : "✓"}</span>{toast.message}
      </div>)}
    </div>
  </ToastContext.Provider>;
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) throw new Error("useToast должен использоваться внутри ToastProvider.");
  return context;
}
