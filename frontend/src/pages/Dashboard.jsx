import React from "react";
import {
  UtensilsCrossed,
  Apple,
  ShieldCheck,
  ChefHat,
  CalendarHeart,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  TrendingUp,
  History,
  Activity
} from "lucide-react";

export default function Dashboard({ onNavigate, stats, aiStatus, recentActivity }) {
  const isAiLive = aiStatus?.ai_configured;

  const modules = [
    {
      id: "food-recognition",
      title: "AI Food Recognition & Nutrition",
      description: "Upload food photos to identify dishes, estimate calories, calculate macronutrients, and view ingredient breakdowns.",
      icon: UtensilsCrossed,
      color: "var(--brand-primary)",
      badge: "Multimodal AI"
    },
    {
      id: "freshness-check",
      title: "Food Freshness Assessment",
      description: "Evaluate produce quality, surface oxidation, discoloration, and mold cues with actionable shelf life advice.",
      icon: Apple,
      color: "var(--brand-secondary)",
      badge: "Quality Grading"
    },
    {
      id: "hygiene-monitor",
      title: "Restaurant Hygiene Inspector",
      description: "Screen commercial kitchen photos or short videos using OpenCV keyframe extraction and sanitation hazard detection.",
      icon: ShieldCheck,
      color: "var(--brand-accent)",
      badge: "OpenCV + Vision"
    },
    {
      id: "cooking-assistant",
      title: "Smart Cooking Assistant",
      description: "Interactive chef assistant that transforms pantry ingredients into balanced recipes with smart dietary substitutions.",
      icon: ChefHat,
      color: "#2A9D8F",
      badge: "Conversational"
    },
    {
      id: "meal-planner",
      title: "Personalized Nutrition Planner",
      description: "Generate tailored 7-day meal plans with Mifflin-St Jeor TDEE calculations, grocery lists, and macro goals.",
      icon: CalendarHeart,
      color: "#E76F51",
      badge: "Adaptive Diet"
    }
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
      {/* Welcome Banner */}
      <div
        style={{
          background: "linear-gradient(135deg, var(--brand-primary), var(--brand-secondary))",
          borderRadius: "var(--radius-xl)",
          padding: "36px 32px",
          color: "#FFFFFF",
          position: "relative",
          overflow: "hidden",
          boxShadow: "var(--shadow-md)"
        }}
      >
        <div style={{ maxWidth: "720px", position: "relative", zIndex: 2 }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
              padding: "4px 12px",
              borderRadius: "999px",
              backgroundColor: "rgba(255, 255, 255, 0.15)",
              fontSize: "0.8rem",
              fontWeight: 600,
              marginBottom: "14px",
              backdropFilter: "blur(4px)"
            }}
          >
            {isAiLive ? <CheckCircle2 size={13} /> : <Sparkles size={13} />}
            <span>{isAiLive ? "Google Gemini Vision AI Connected" : "Intelligent Demo Simulation Mode Active"}</span>
          </div>

          <h1 style={{ fontSize: "2.2rem", fontWeight: 800, letterSpacing: "-0.03em", lineHeight: 1.15 }}>
            Welcome to Food Verse AI
          </h1>
          <p style={{ fontSize: "1.05rem", opacity: 0.9, marginTop: "10px", lineHeight: 1.5 }}>
            "Smarter Food Choices. Safer Kitchens. Healthier Living." An end-to-end multimodal food intelligence
            platform combining vision recognition, freshness grading, hygiene auditing, and dietary planning.
          </p>

          <div style={{ display: "flex", gap: "12px", marginTop: "22px", flexWrap: "wrap" }}>
            <button
              onClick={() => onNavigate("food-recognition")}
              className="btn btn-accent"
              style={{ padding: "12px 22px", fontSize: "0.95rem" }}
            >
              <UtensilsCrossed size={17} /> Scan Food Image
            </button>
            <button
              onClick={() => onNavigate("meal-planner")}
              className="btn"
              style={{
                backgroundColor: "rgba(255, 255, 255, 0.15)",
                color: "#FFFFFF",
                backdropFilter: "blur(4px)",
                padding: "12px 20px"
              }}
            >
              <CalendarHeart size={17} /> Build 7-Day Meal Plan
            </button>
          </div>
        </div>
      </div>

      {/* Summary KPI Metric Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "16px"
        }}
      >
        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase" }}>
              Total Analyses
            </span>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "var(--brand-light)", color: "var(--brand-primary)" }}>
              <Activity size={18} />
            </div>
          </div>
          <div style={{ fontSize: "1.8rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            {stats?.totalAnalyses || 0}
          </div>
          <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)" }}>
            Saved in local SQLite store
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase" }}>
              Food Scans
            </span>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "rgba(224, 122, 95, 0.15)", color: "var(--brand-accent)" }}>
              <UtensilsCrossed size={18} />
            </div>
          </div>
          <div style={{ fontSize: "1.8rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            {stats?.foodCount || 0}
          </div>
          <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)" }}>
            Nutrition & calorie estimations
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase" }}>
              Freshness Checks
            </span>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "rgba(45, 106, 79, 0.15)", color: "var(--brand-secondary)" }}>
              <Apple size={18} />
            </div>
          </div>
          <div style={{ fontSize: "1.8rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            {stats?.freshnessCount || 0}
          </div>
          <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)" }}>
            Produce quality assessments
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase" }}>
              Hygiene Audits
            </span>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "rgba(2, 132, 199, 0.15)", color: "var(--status-info)" }}>
              <ShieldCheck size={18} />
            </div>
          </div>
          <div style={{ fontSize: "1.8rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            {stats?.hygieneCount || 0}
          </div>
          <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)" }}>
            Kitchen sanitation reviews
          </span>
        </div>
      </div>

      {/* Module Launchpad Grid */}
      <div>
        <div style={{ marginBottom: "16px" }}>
          <h2 style={{ fontSize: "1.35rem", fontWeight: 800, color: "var(--text-primary)" }}>
            Explore Core Intelligence Modules
          </h2>
          <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)" }}>
            Select any module to start an image scan, audit a kitchen, chat for recipes, or generate custom diets.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "20px"
          }}
        >
          {modules.map((m) => {
            const Icon = m.icon;
            return (
              <div
                key={m.id}
                className="card"
                onClick={() => onNavigate(m.id)}
                style={{
                  cursor: "pointer",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  gap: "16px"
                }}
              >
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
                    <div
                      style={{
                        width: "44px",
                        height: "44px",
                        borderRadius: "var(--radius-sm)",
                        backgroundColor: "var(--brand-light)",
                        color: m.color,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center"
                      }}
                    >
                      <Icon size={22} />
                    </div>
                    <span className="badge badge-neutral">{m.badge}</span>
                  </div>

                  <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-primary)" }}>
                    {m.title}
                  </h3>
                  <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", marginTop: "6px", lineHeight: 1.45 }}>
                    {m.description}
                  </p>
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    color: "var(--brand-primary)",
                    fontWeight: 600,
                    fontSize: "0.88rem",
                    paddingTop: "10px",
                    borderTop: "1px solid var(--border-color)"
                  }}
                >
                  <span>Launch Module</span>
                  <ArrowRight size={15} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Activity List */}
      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
          <div>
            <h3 style={{ fontSize: "1.15rem", fontWeight: 800, color: "var(--text-primary)" }}>
              Recent Activity Feed
            </h3>
            <span style={{ fontSize: "0.82rem", color: "var(--text-muted)" }}>
              Latest analysis and scanner executions
            </span>
          </div>

          <button
            onClick={() => onNavigate("history")}
            className="btn btn-outline"
            style={{ padding: "6px 14px", fontSize: "0.82rem" }}
          >
            <History size={15} /> View Full History
          </button>
        </div>

        {recentActivity && recentActivity.length > 0 ? (
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {recentActivity.slice(0, 5).map((act) => (
              <div
                key={act.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "12px 14px",
                  borderRadius: "var(--radius-sm)",
                  backgroundColor: "var(--bg-card-subtle)",
                  border: "1px solid var(--border-color)",
                  flexWrap: "wrap",
                  gap: "10px"
                }}
              >
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span className="badge badge-neutral" style={{ textTransform: "capitalize" }}>
                      {act.module_type}
                    </span>
                    <strong style={{ fontSize: "0.92rem", color: "var(--text-primary)" }}>
                      {act.title}
                    </strong>
                    {act.is_demo && (
                      <span className="badge badge-demo" style={{ fontSize: "0.68rem" }}>
                        Demo
                      </span>
                    )}
                  </div>
                  <p style={{ fontSize: "0.8rem", color: "var(--text-secondary)", marginTop: "2px" }}>
                    {act.summary}
                  </p>
                </div>

                <span style={{ fontSize: "0.76rem", color: "var(--text-muted)" }}>
                  {new Date(act.created_at).toLocaleDateString()} {new Date(act.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ textAlign: "center", padding: "32px 16px", color: "var(--text-muted)", fontSize: "0.9rem" }}>
            No analyses recorded yet. Try uploading a food photo in Food Recognition or Freshness Check!
          </div>
        )}
      </div>
    </div>
  );
}
