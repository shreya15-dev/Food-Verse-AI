import React from "react";
import { Info, Leaf, Cpu, Database, ShieldCheck, HeartPulse, Layers, Sparkles } from "lucide-react";

export default function AboutPage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "28px", maxWidth: "1000px" }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <Info size={28} color="var(--brand-primary)" />
            About Food Verse AI
          </h1>
          <p className="page-description">
            "Smarter Food Choices. Safer Kitchens. Healthier Living." An academic capstone engineering project
            exploring multimodal artificial intelligence for culinary and public health applications.
          </p>
        </div>
      </div>

      {/* Mission & Problem Statement */}
      <div className="card">
        <h2 style={{ fontSize: "1.3rem", fontWeight: 800, color: "var(--brand-primary)", marginBottom: "12px" }}>
          Problem Statement & Motivation
        </h2>
        <p style={{ fontSize: "0.94rem", color: "var(--text-secondary)", lineHeight: 1.6 }}>
          Modern eating habits face three intertwined challenges: <strong>nutritional obscurity</strong> (difficulty
          tracking exact macro and calorie intake across diverse home-cooked or restaurant meals), <strong>preventable food waste</strong>
          (premature disposal of cosmetically imperfect yet nutritious produce alongside accidental spoilage), and
          <strong>commercial food safety oversight</strong> (difficulty maintaining consistent sanitation standards across commercial prep kitchens).
        </p>
        <p style={{ fontSize: "0.94rem", color: "var(--text-secondary)", lineHeight: 1.6, marginTop: "12px" }}>
          <strong>Food Verse AI</strong> addresses these hurdles through a unified multimodal platform combining computer vision,
          image & video processing, conversational recipe modeling, and individualized macronutrient planning.
        </p>
      </div>

      {/* Architecture & Tech Stack Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "16px"
        }}
      >
        <div className="card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "var(--brand-light)", color: "var(--brand-primary)" }}>
              <Layers size={20} />
            </div>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700 }}>Frontend Architecture</h3>
          </div>
          <ul style={{ paddingLeft: "18px", fontSize: "0.86rem", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "6px" }}>
            <li><strong>React 19 & Vite</strong>: Ultra-fast module bundling and hot module reloading.</li>
            <li><strong>Custom CSS Design System</strong>: Responsive SaaS layouts, CSS variables, dark/light theme toggle.</li>
            <li><strong>Zero Paid UI Bloat</strong>: Clean native component styling with Lucide icons.</li>
            <li><strong>Print stylesheets</strong>: Custom formatted output for meal plans and receipts.</li>
          </ul>
        </div>

        <div className="card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "rgba(224, 122, 95, 0.15)", color: "var(--brand-accent)" }}>
              <Cpu size={20} />
            </div>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700 }}>Backend & Processing</h3>
          </div>
          <ul style={{ paddingLeft: "18px", fontSize: "0.86rem", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "6px" }}>
            <li><strong>Python Flask REST API</strong>: Clean JSON endpoints and validation.</li>
            <li><strong>OpenCV (cv2)</strong>: Automated keyframe extraction from MP4/WEBM kitchen video clips.</li>
            <li><strong>Pillow (PIL)</strong>: In-memory image analysis, dimension extraction, and color palette evaluation.</li>
            <li><strong>Temporary file security</strong>: Atomic temp handling with deterministic cleanup.</li>
          </ul>
        </div>

        <div className="card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
            <div style={{ padding: "8px", borderRadius: "var(--radius-sm)", backgroundColor: "rgba(45, 106, 79, 0.15)", color: "var(--brand-secondary)" }}>
              <Database size={20} />
            </div>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700 }}>Data & AI Integration</h3>
          </div>
          <ul style={{ paddingLeft: "18px", fontSize: "0.86rem", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "6px" }}>
            <li><strong>SQLite Store</strong>: Local persistence for scan logs, weekly plans, and profile settings.</li>
            <li><strong>Google Gemini Vision API</strong>: Optional live vision recognition via environment variable.</li>
            <li><strong>Zero-Credential Fallback</strong>: High-fidelity heuristic demo engine ensuring 100% functionality offline.</li>
            <li><strong>Honest AI Badging</strong>: Transparent badges distinguishing simulation from live AI.</li>
          </ul>
        </div>
      </div>

      {/* Ethical AI & Safety Principles */}
      <div className="card">
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "14px" }}>
          <ShieldCheck size={22} color="var(--brand-accent)" />
          <h2 style={{ fontSize: "1.2rem", fontWeight: 800, color: "var(--text-primary)" }}>
            Ethical AI & Food Safety Guardrails
          </h2>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "10px", fontSize: "0.9rem", color: "var(--text-secondary)", lineHeight: 1.55 }}>
          <p>
            1. <strong>No False Precision</strong>: Image-based nutrient calculators approximate values based on visible surface area. Cooking oils, hidden sugars, and specific sodium content cannot be measured by a camera alone.
          </p>
          <p>
            2. <strong>Microbiological Limitations</strong>: Spoilage bacteria (like Salmonella, E. coli, Listeria) and heat-resistant toxins can exist without causing visible browning or mold. The platform explicitly cautions users never to rely solely on camera images for food safety.
          </p>
          <p>
            3. <strong>Advisory, Not Regulatory</strong>: The hygiene inspector provides preliminary observational checklists for operational kitchen improvement, not legal municipal inspection certification.
          </p>
          <p>
            4. <strong>Evidence-Based Nutritional Modeling</strong>: The meal planner strictly implements established Mifflin-St Jeor formulas with healthy caloric floors, preventing extreme or dangerous crash diets.
          </p>
        </div>
      </div>
    </div>
  );
}
