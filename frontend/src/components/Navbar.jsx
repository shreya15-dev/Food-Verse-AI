import React from "react";
import { Menu, Sun, Moon, Sparkles, AlertCircle, CheckCircle2 } from "lucide-react";

export default function Navbar({
  theme,
  toggleTheme,
  onMobileMenuToggle,
  aiStatus,
  currentPageTitle
}) {
  const isDark = theme === "dark";
  const isAiLive = aiStatus?.ai_configured;

  return (
    <header className="app-header">
      <div className="header-left">
        <button
          className="mobile-menu-btn"
          onClick={onMobileMenuToggle}
          aria-label="Toggle Navigation Menu"
        >
          <Menu size={22} />
        </button>
        <div className="header-greeting">
          <h1 className="header-title">{currentPageTitle || "Dashboard"}</h1>
          <span className="header-subtitle">Food Verse AI Multimodal Food Intelligence</span>
        </div>
      </div>

      <div className="header-right">
        {/* System Mode Indicator */}
        <div
          className={`badge ${isAiLive ? "badge-live" : "badge-demo"}`}
          title={
            isAiLive
              ? "Connected to Live Gemini Vision Model"
              : "Running in Smart Heuristic Demo Fallback Mode (No API key required)"
          }
        >
          {isAiLive ? (
            <>
              <CheckCircle2 size={13} />
              <span>Live Vision AI Active</span>
            </>
          ) : (
            <>
              <Sparkles size={13} />
              <span>Demo Simulation Mode</span>
            </>
          )}
        </div>

        {/* Theme Toggle */}
        <button
          className="theme-toggle-btn"
          onClick={toggleTheme}
          title={isDark ? "Switch to Light Theme" : "Switch to Dark Theme"}
          aria-label="Toggle Color Theme"
        >
          {isDark ? <Sun size={18} /> : <Moon size={18} />}
        </button>

        {/* User Profile Placeholder */}
        <div className="user-profile-badge">
          <div className="avatar-circle">FV</div>
          <span className="user-name-text">Researcher / Student</span>
        </div>
      </div>
    </header>
  );
}
