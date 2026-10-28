import React from "react";
import { Leaf, Heart } from "lucide-react";

export default function Footer({ onNavigate }) {
  return (
    <footer
      style={{
        marginTop: "auto",
        borderTop: "1px solid var(--border-color)",
        backgroundColor: "var(--bg-card)",
        padding: "28px 32px",
        transition: "var(--transition)"
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "20px",
          maxWidth: "1300px",
          margin: "0 auto"
        }}
      >
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span
              style={{
                display: "inline-flex",
                color: "var(--brand-primary)",
                fontWeight: 700,
                fontSize: "1.05rem"
              }}
            >
              <Leaf size={18} style={{ marginRight: 6 }} /> Food Verse AI
            </span>
          </div>
          <p
            style={{
              fontSize: "0.85rem",
              color: "var(--text-secondary)",
              marginTop: "4px"
            }}
          >
            "Smarter Food Choices. Safer Kitchens. Healthier Living."
          </p>
        </div>

        <div style={{ display: "flex", gap: "20px", fontSize: "0.86rem", color: "var(--text-secondary)" }}>
          <button
            onClick={() => onNavigate("about")}
            style={{ background: "none", color: "inherit", textDecoration: "underline" }}
          >
            About
          </button>
          <button
            onClick={() => onNavigate("help")}
            style={{ background: "none", color: "inherit", textDecoration: "underline" }}
          >
            User Guide
          </button>
          <button
            onClick={() => onNavigate("dashboard")}
            style={{ background: "none", color: "inherit", textDecoration: "underline" }}
          >
            Dashboard
          </button>
        </div>
      </div>

      <div
        style={{
          maxWidth: "1300px",
          margin: "18px auto 0",
          paddingTop: "16px",
          borderTop: "1px dashed var(--border-color)",
          fontSize: "0.76rem",
          color: "var(--text-muted)",
          lineHeight: 1.5,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "10px"
        }}
      >
        <span>
          Academic Capstone Project • Designed for educational and demonstration purposes.
          Estimates are algorithmic approximations and not medical or regulatory certification.
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
          Crafted with <Heart size={13} color="#E07A5F" fill="#E07A5F" /> for Health & Safety
        </span>
      </div>
    </footer>
  );
}
