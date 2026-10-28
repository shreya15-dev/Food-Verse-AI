import React, { createContext, useContext, useState, useCallback } from "react";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "info", duration = 4000) => {
    const id = Date.now() + Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);

    if (duration > 0) {
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, duration);
    }
  }, []);

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <div
        style={{
          position: "fixed",
          bottom: "24px",
          right: "24px",
          display: "flex",
          flexDirection: "column",
          gap: "10px",
          zIndex: 9999,
          maxWidth: "380px"
        }}
      >
        {toasts.map((toast) => {
          let bgColor = "var(--bg-card)";
          let borderColor = "var(--border-color)";
          let icon = <Info size={18} color="var(--status-info)" />;

          if (toast.type === "success") {
            borderColor = "var(--status-success)";
            icon = <CheckCircle2 size={18} color="var(--status-success)" />;
          } else if (toast.type === "error") {
            borderColor = "var(--status-danger)";
            icon = <AlertCircle size={18} color="var(--status-danger)" />;
          }

          return (
            <div
              key={toast.id}
              className="card"
              style={{
                padding: "12px 16px",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                borderLeft: `4px solid ${borderColor}`,
                boxShadow: "var(--shadow-md)"
              }}
            >
              {icon}
              <span style={{ fontSize: "0.88rem", flex: 1, color: "var(--text-primary)" }}>
                {toast.message}
              </span>
              <button
                onClick={() => removeToast(toast.id)}
                style={{ background: "none", color: "var(--text-muted)", padding: "2px" }}
              >
                <X size={15} />
              </button>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    return { addToast: (msg) => console.log("Toast fallback:", msg) };
  }
  return context;
}
