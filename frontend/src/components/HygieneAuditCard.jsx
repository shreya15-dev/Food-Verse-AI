import React, { useState } from "react";
import { ShieldCheck, AlertCircle, AlertTriangle, CheckCircle, Video, Eye, Sparkles } from "lucide-react";

export default function HygieneAuditCard({ data }) {
  if (!data) return null;

  const {
    hygiene_score = 85,
    preliminary_grade = "Grade B",
    summary = "Kitchen inspection complete.",
    observations = [],
    positive_points = [],
    keyframes = [],
    is_video = false,
    is_demo = true,
    analysis_mode = "Computer Vision Fallback",
    disclaimer = ""
  } = data;

  const [activeKeyframe, setActiveKeyframe] = useState(null);

  const getSeverityBadge = (severity) => {
    const s = (severity || "").toLowerCase();
    if (s === "high") {
      return (
        <span className="badge badge-danger">
          <AlertCircle size={13} /> High Priority
        </span>
      );
    }
    if (s === "medium") {
      return (
        <span className="badge badge-warning">
          <AlertTriangle size={13} /> Medium Attention
        </span>
      );
    }
    return (
      <span className="badge badge-success">
        <CheckCircle size={13} /> Low / Minor
      </span>
    );
  };

  const getGradeColor = () => {
    if (hygiene_score >= 85) return "var(--status-success)";
    if (hygiene_score >= 70) return "var(--status-warning)";
    return "var(--status-danger)";
  };

  return (
    <div className="card" style={{ display: "flex", flexDirection: "column", gap: "22px" }}>
      {/* Header Summary */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "12px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            <span className="badge badge-neutral">
              {is_video ? <Video size={13} /> : <Eye size={13} />}
              {is_video ? "Video Frame Inspection" : "Still Kitchen Image"}
            </span>
            <span className={`badge ${is_demo ? "badge-demo" : "badge-live"}`}>
              <Sparkles size={12} /> {analysis_mode}
            </span>
          </div>
          <h2 style={{ fontSize: "1.5rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            Commercial Kitchen Hygiene Audit
          </h2>
          <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", marginTop: "4px", maxWidth: "750px" }}>
            {summary}
          </p>
        </div>

        {/* Score & Grade Card */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "14px",
            padding: "12px 20px",
            backgroundColor: "var(--bg-card-subtle)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--border-color)"
          }}
        >
          <div style={{ textAlign: "right" }}>
            <span style={{ fontSize: "0.72rem", color: "var(--text-muted)", fontWeight: 700, textTransform: "uppercase" }}>
              Sanitation Grade
            </span>
            <div style={{ fontSize: "1.3rem", fontWeight: 800, color: getGradeColor() }}>
              {preliminary_grade}
            </div>
          </div>
          <div style={{ width: "1px", height: "35px", backgroundColor: "var(--border-color)" }} />
          <div>
            <span style={{ fontSize: "0.72rem", color: "var(--text-muted)", fontWeight: 700, textTransform: "uppercase" }}>
              Cleanliness Score
            </span>
            <div style={{ fontSize: "1.6rem", fontWeight: 900, color: "var(--text-primary)", lineHeight: 1 }}>
              {hygiene_score} <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", fontWeight: 500 }}>/ 100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Video Keyframes Gallery (if video processed) */}
      {is_video && keyframes && keyframes.length > 0 && (
        <div style={{ padding: "16px", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
            <h4 style={{ fontSize: "0.92rem", fontWeight: 700, color: "var(--text-primary)", display: "flex", alignItems: "center", gap: "6px" }}>
              <Video size={16} color="var(--brand-primary)" /> OpenCV Extracted Keyframes ({keyframes.length})
            </h4>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)" }}>
              Sampled across video timeline
            </span>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "10px" }}>
            {keyframes.map((kf, i) => (
              <div
                key={i}
                onClick={() => setActiveKeyframe(kf)}
                style={{
                  position: "relative",
                  borderRadius: "var(--radius-sm)",
                  overflow: "hidden",
                  cursor: "pointer",
                  border: "2px solid var(--border-color)",
                  transition: "var(--transition)"
                }}
                title={`Frame at ${kf.timestamp_str} (click to inspect)`}
              >
                <img
                  src={kf.image_data_url}
                  alt={`Keyframe ${i + 1}`}
                  style={{ width: "100%", height: "90px", objectFit: "cover", display: "block" }}
                />
                <span
                  style={{
                    position: "absolute",
                    bottom: "4px",
                    right: "4px",
                    backgroundColor: "rgba(0,0,0,0.75)",
                    color: "#fff",
                    fontSize: "0.68rem",
                    padding: "2px 6px",
                    borderRadius: "4px",
                    fontWeight: 600
                  }}
                >
                  {kf.timestamp_str}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Observation Cards */}
      <div>
        <h4 style={{ fontSize: "1.05rem", fontWeight: 800, color: "var(--text-primary)", marginBottom: "14px" }}>
          Specific Risk Factors & Advisory Findings ({observations.length})
        </h4>

        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          {observations.map((obs, idx) => (
            <div
              key={idx}
              style={{
                padding: "16px 18px",
                borderRadius: "var(--radius-md)",
                backgroundColor: "var(--bg-card-subtle)",
                border: "1px solid var(--border-color)",
                display: "flex",
                flexDirection: "column",
                gap: "8px"
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "8px" }}>
                <span style={{ fontSize: "0.85rem", fontWeight: 700, color: "var(--text-primary)" }}>
                  {obs.category}
                </span>
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  {obs.video_timestamp && (
                    <span className="badge badge-neutral" style={{ fontSize: "0.75rem" }}>
                      Timestamp: {obs.video_timestamp}
                    </span>
                  )}
                  {getSeverityBadge(obs.severity)}
                </div>
              </div>

              <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", lineHeight: 1.45 }}>
                <strong>Finding:</strong> {obs.finding}
              </p>

              <div
                style={{
                  marginTop: "4px",
                  padding: "8px 12px",
                  borderRadius: "var(--radius-sm)",
                  backgroundColor: "var(--brand-light)",
                  fontSize: "0.84rem",
                  color: "var(--brand-primary)"
                }}
              >
                <strong>Corrective Action:</strong> {obs.corrective_action}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Positive Practices */}
      {positive_points && positive_points.length > 0 && (
        <div style={{ padding: "16px 20px", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
          <h4 style={{ fontSize: "0.92rem", fontWeight: 700, color: "var(--status-success)", marginBottom: "8px", display: "flex", alignItems: "center", gap: "6px" }}>
            <CheckCircle size={16} /> Observed Compliant & Positive Practices
          </h4>
          <ul style={{ paddingLeft: "20px", fontSize: "0.86rem", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "4px" }}>
            {positive_points.map((pt, i) => (
              <li key={i}>{pt}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Official Health Inspection Disclaimer */}
      {disclaimer && (
        <div className="disclaimer-box">
          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontWeight: 700, marginBottom: "4px" }}>
            <ShieldCheck size={16} color="var(--brand-accent)" /> Official Advisory Notice
          </div>
          <p>{disclaimer}</p>
        </div>
      )}
    </div>
  );
}
