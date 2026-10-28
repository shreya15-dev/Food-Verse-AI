import React from "react";
import {
  LayoutDashboard,
  UtensilsCrossed,
  Apple,
  ShieldCheck,
  ChefHat,
  CalendarHeart,
  History,
  Info,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Leaf
} from "lucide-react";

export default function Sidebar({
  activeTab,
  setActiveTab,
  collapsed,
  setCollapsed,
  mobileOpen,
  setMobileOpen
}) {
  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "food-recognition", label: "Food Recognition", icon: UtensilsCrossed, badge: "AI" },
    { id: "freshness-check", label: "Freshness Assessment", icon: Apple },
    { id: "hygiene-monitor", label: "Hygiene Inspector", icon: ShieldCheck, badge: "OpenCV" },
    { id: "cooking-assistant", label: "Cooking Assistant", icon: ChefHat },
    { id: "meal-planner", label: "Nutrition & Meal Plan", icon: CalendarHeart },
    { id: "history", label: "Analysis History", icon: History },
  ];

  const infoItems = [
    { id: "about", label: "About Project", icon: Info },
    { id: "help", label: "Help & Guide", icon: HelpCircle },
  ];

  const handleSelect = (id) => {
    setActiveTab(id);
    if (setMobileOpen) setMobileOpen(false);
  };

  return (
    <aside
      className={`app-sidebar ${collapsed ? "collapsed" : ""} ${
        mobileOpen ? "mobile-open" : ""
      }`}
    >
      <div className="sidebar-header">
        <a
          href="#dashboard"
          onClick={(e) => {
            e.preventDefault();
            handleSelect("dashboard");
          }}
          className="brand-logo-area"
          title="Food Verse AI"
        >
          <div className="brand-icon-box">
            <Leaf size={22} />
          </div>
          {!collapsed && (
            <div className="brand-text-box">
              <span className="brand-name">Food Verse AI</span>
              <span className="brand-tagline-mini">Food Intelligence</span>
            </div>
          )}
        </a>

        <button
          className="sidebar-toggle-btn"
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          aria-label="Toggle Sidebar"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="sidebar-nav">
        {!collapsed && <div className="nav-section-label">Core Modules</div>}
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? "active" : ""}`}
              onClick={() => handleSelect(item.id)}
              title={collapsed ? item.label : ""}
            >
              <Icon size={20} className="nav-icon" />
              {!collapsed && <span>{item.label}</span>}
              {!collapsed && item.badge && (
                <span className="nav-badge-pill">{item.badge}</span>
              )}
            </button>
          );
        })}

        {!collapsed && <div className="nav-section-label">Documentation</div>}
        {infoItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? "active" : ""}`}
              onClick={() => handleSelect(item.id)}
              title={collapsed ? item.label : ""}
            >
              <Icon size={20} className="nav-icon" />
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        {!collapsed ? (
          <div style={{ fontSize: "0.74rem", color: "var(--text-muted)", lineHeight: 1.35 }}>
            <div style={{ fontWeight: 600, color: "var(--text-secondary)" }}>
              Academic Submission Build
            </div>
            <span>v1.0.0 • College Capstone</span>
          </div>
        ) : (
          <div style={{ textAlign: "center", fontSize: "0.7rem", color: "var(--text-muted)" }}>
            v1.0
          </div>
        )}
      </div>
    </aside>
  );
}
