import React, { useState, useEffect } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Footer from "./components/Footer";
import { ToastProvider } from "./components/Toast";

import Dashboard from "./pages/Dashboard";
import FoodRecognition from "./pages/FoodRecognition";
import FreshnessCheck from "./pages/FreshnessCheck";
import HygieneMonitor from "./pages/HygieneMonitor";
import CookingAssistant from "./pages/CookingAssistant";
import MealPlanner from "./pages/MealPlanner";
import HistoryPage from "./pages/HistoryPage";
import AboutPage from "./pages/AboutPage";
import HelpPage from "./pages/HelpPage";

import { checkHealth, getHistory } from "./services/api";

function AppContent() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("foodverse_theme") || "light";
  });
  const [aiStatus, setAiStatus] = useState(null);
  const [stats, setStats] = useState({
    totalAnalyses: 0,
    foodCount: 0,
    freshnessCount: 0,
    hygieneCount: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("foodverse_theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  // Fetch API Health & SQLite Stats on mount
  const refreshStats = async () => {
    const health = await checkHealth();
    if (health?.status === "healthy") {
      setAiStatus(health);
    }

    const historyRes = await getHistory(50);
    if (historyRes?.success && historyRes?.data) {
      const items = historyRes.data;
      setRecentActivity(items);
      const foodCount = items.filter((i) => i.module_type === "food").length;
      const freshnessCount = items.filter((i) => i.module_type === "freshness").length;
      const hygieneCount = items.filter((i) => i.module_type === "hygiene").length;

      setStats({
        totalAnalyses: items.length,
        foodCount,
        freshnessCount,
        hygieneCount
      });
    }
  };

  useEffect(() => {
    refreshStats();
  }, []);

  const getPageTitle = () => {
    switch (activeTab) {
      case "dashboard":
        return "Dashboard Overview";
      case "food-recognition":
        return "AI Food Recognition & Nutrition";
      case "freshness-check":
        return "Food Freshness Assessment";
      case "hygiene-monitor":
        return "Restaurant Hygiene Inspector";
      case "cooking-assistant":
        return "Smart Cooking Assistant";
      case "meal-planner":
        return "Personalized Nutrition Planner";
      case "history":
        return "Analysis Scan History";
      case "about":
        return "About Food Verse AI";
      case "help":
        return "User Guide & Documentation";
      default:
        return "Food Verse AI";
    }
  };

  return (
    <div className="app-container">
      {/* Mobile Drawer Backdrop */}
      <div
        className={`mobile-overlay ${mobileOpen ? "visible" : ""}`}
        onClick={() => setMobileOpen(false)}
      />

      {/* Collapsible Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
        mobileOpen={mobileOpen}
        setMobileOpen={setMobileOpen}
      />

      {/* Main Shell */}
      <div className={`app-main ${collapsed ? "collapsed" : ""}`}>
        <Navbar
          theme={theme}
          toggleTheme={toggleTheme}
          onMobileMenuToggle={() => setMobileOpen(!mobileOpen)}
          aiStatus={aiStatus}
          currentPageTitle={getPageTitle()}
        />

        <main className="app-content">
          {activeTab === "dashboard" && (
            <Dashboard
              onNavigate={setActiveTab}
              stats={stats}
              aiStatus={aiStatus}
              recentActivity={recentActivity}
            />
          )}
          {activeTab === "food-recognition" && (
            <FoodRecognition onScanCompleted={refreshStats} />
          )}
          {activeTab === "freshness-check" && (
            <FreshnessCheck onScanCompleted={refreshStats} />
          )}
          {activeTab === "hygiene-monitor" && (
            <HygieneMonitor onScanCompleted={refreshStats} />
          )}
          {activeTab === "cooking-assistant" && <CookingAssistant />}
          {activeTab === "meal-planner" && <MealPlanner />}
          {activeTab === "history" && <HistoryPage />}
          {activeTab === "about" && <AboutPage />}
          {activeTab === "help" && <HelpPage />}
        </main>

        <Footer onNavigate={setActiveTab} />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  );
}
