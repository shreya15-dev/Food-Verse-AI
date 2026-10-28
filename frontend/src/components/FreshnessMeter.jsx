import React from "react";
import { CheckCircle2, AlertTriangle, XCircle, ShieldAlert, Sparkles, Clock, Lightbulb, Info } from "lucide-react";

export default function FreshnessMeter({ data }) {
  if (!data) return null;

  const {
    item_identified = "Organic Produce Item",
    category = "Looks fresh",
    status_color = "success",
    freshness_score = 88,
    confidence = 0.88,
    observations = [],
    shelf_life_estimate = "3-5 days",
    recommendation = "",
    storage_tips = [],
    is_demo = true,
    analysis_mode = "Simulation Fallback",
    disclaimer = ""
  } = data;

  const getStatusBadge = () => {
    switch (category) {
      case "Looks fresh":
        return (
          <span className="badge badge-success" style={{ fontSize: "0.9rem", padding: "6px 14px" }}>
            <CheckCircle2 size={16} /> Looks Fresh
          </span>
        );
      case "Possible deterioration":
        return (
          <span className="badge badge-warning" style={{ fontSize: "0.9rem", padding: "6px 14px" }}>
            <AlertTriangle size={16} /> Possible Deterioration
          </span>
        );
      default:
        return (
          <span className="badge badge-danger" style={{ fontSize: "0.9rem", padding: "6px 14px" }}>
            <XCircle size={16} /> Uncertain / Spoilage Detected
          </span>
        );
    }
  };

  const getScoreColor = () => {
    if (freshness_score >= 80) return "var(--status-success)";
    if (freshness_score >= 50) return "var(--status-warning)";
    return "var(--status-danger)";
  };

  return (
    <div className="card" style={{ display: "flex", flexDirection: "column", gap: "22px" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "12px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            {getStatusBadge()}
            <span className={`badge ${is_demo ? "badge-demo" : "badge-live"}`}>
              <Sparkles size={12} /> {analysis_mode}
            </span>
            <span className="badge badge-neutral">
              Confidence: {Math.round(confidence * 100)}%
            </span>
          </div>
          <h2 style={{ fontSize: "1.5rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            {item_identified}
          </h2>
        </div>

        {/* Freshness Score Ring / Box */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            padding: "10px 18px",
            backgroundColor: "var(--bg-card-subtle)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--border-color)"
          }}
        >
          <div style={{ textAlign: "right" }}>
            <span style={{ fontSize: "0.74rem", color: "var(--text-muted)", fontWeight: 700, textTransform: "uppercase" }}>
              Freshness Index
            </span>
            <div style={{ fontSize: "1.7rem", fontWeight: 900, color: getScoreColor(), lineHeight: 1.1 }}>
              {freshness_score} <span style={{ fontSize: "0.85rem", color: "var(--text-muted)", fontWeight: 500 }}>/ 100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Observations Grid */}
      <div>
        <h4 style={{ fontSize: "1rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
          <Info size={17} color="var(--brand-primary)" /> Visual Assessment Findings
        </h4>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "12px" }}>
          {observations.map((obs, idx) => (
            <div
              key={idx}
              style={{
                padding: "14px 16px",
                backgroundColor: "var(--bg-card-subtle)",
                borderRadius: "var(--radius-sm)",
                border: "1px solid var(--border-color)"
              }}
            >
              <span style={{ fontSize: "0.76rem", fontWeight: 700, color: "var(--brand-secondary)", textTransform: "uppercase" }}>
                {obs.cue}
              </span>
              <p style={{ fontSize: "0.88rem", color: "var(--text-primary)", marginTop: "4px", lineHeight: 1.45 }}>
                {obs.finding}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Actionable Next Steps & Storage Window */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: "14px"
        }}
      >
        <div
          style={{
            padding: "16px",
            borderRadius: "var(--radius-md)",
            backgroundColor: "var(--brand-light)",
            border: "1px solid rgba(45, 106, 79, 0.2)"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 700, color: "var(--brand-primary)", marginBottom: "6px" }}>
            <Clock size={16} /> Estimated Usable Window
          </div>
          <p style={{ fontSize: "0.9rem", color: "var(--text-primary)", fontWeight: 600 }}>
            {shelf_life_estimate}
          </p>
          <p style={{ fontSize: "0.82rem", color: "var(--text-secondary)", marginTop: "4px" }}>
            {recommendation}
          </p>
        </div>

        {storage_tips && storage_tips.length > 0 && (
          <div
            style={{
              padding: "16px",
              borderRadius: "var(--radius-md)",
              backgroundColor: "var(--bg-card-subtle)",
              border: "1px solid var(--border-color)"
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 700, color: "var(--text-primary)", marginBottom: "6px" }}>
              <Lightbulb size={16} color="var(--brand-accent)" /> Recommended Storage Practice
            </div>
            <ul style={{ paddingLeft: "18px", fontSize: "0.84rem", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "4px" }}>
              {storage_tips.map((tip, idx) => (
                <li key={idx}>{tip}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Safety Disclaimer */}
      {disclaimer && (
        <div className="disclaimer-box">
          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontWeight: 700, marginBottom: "4px", color: "var(--status-danger)" }}>
            <ShieldAlert size={16} /> Food Safety & Spoilage Limitation Notice
          </div>
          <p>{disclaimer}</p>
        </div>
      )}
    </div>
  );
}
