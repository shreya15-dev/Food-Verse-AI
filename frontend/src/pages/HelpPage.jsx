import React, { useState } from "react";
import { HelpCircle, ChevronDown, ChevronUp, Camera, Video, Sparkles, BookOpen, Check } from "lucide-react";

export default function HelpPage() {
  const [openFaq, setOpenFaq] = useState(0);

  const faqs = [
    {
      q: "Do I need to sign up or enter a paid API key to run this application?",
      a: "No! Food Verse AI is built with a zero-credential demo engine. All modules (food recognition, freshness analysis, hygiene audit, cooking assistant, and meal planner) work completely offline out of the box. If an evaluator sets GEMINI_API_KEY in backend/.env, the system automatically unlocks live multimodal vision."
    },
    {
      q: "How does the Food Recognition module calculate calories?",
      a: "The module uses vision analysis to identify the primary dish, portion size estimate, and ingredient list. When live Gemini Vision is connected, it retrieves recognized recipe breakdowns. In demo mode, it uses deterministic computer vision color heuristics and a verified catalog of recipes."
    },
    {
      q: "What video formats are supported in Restaurant Hygiene Monitoring?",
      a: "We support MP4, WEBM, and MOV video clips up to 35 MB. Using OpenCV (cv2.VideoCapture), the backend automatically extracts representative keyframes across the video duration and analyzes them for prep station cleanliness, uncovered food items, and clutter."
    },
    {
      q: "Can this app guarantee that my food is completely safe to eat?",
      a: "No. Visual inspection cannot identify microscopic bacterial pathogens (like Salmonella, Listeria, or E. coli), odorless spoilage, or chemical toxins. When food smells off, tastes unusual, or has been left at room temperature for extended periods, always err on the side of caution and discard it."
    },
    {
      q: "How does the Personalized Meal Planner compute my calorie target?",
      a: "It implements the clinically validated Mifflin-St Jeor formula to determine your Basal Metabolic Rate (BMR), applies an activity multiplier to compute Total Daily Energy Expenditure (TDEE), and applies safe, conservative adjustments based on your goal."
    }
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "28px", maxWidth: "1000px" }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <HelpCircle size={28} color="var(--brand-primary)" />
            Help & User Guide
          </h1>
          <p className="page-description">
            Everything you need to know about capturing photos, interpreting analysis reports,
            configuring video audits, and using Food Verse AI effectively.
          </p>
        </div>
      </div>

      {/* Photography & Media Best Practices */}
      <div className="card">
        <h2 style={{ fontSize: "1.2rem", fontWeight: 800, color: "var(--brand-primary)", marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
          <Camera size={20} /> Tips for High-Accuracy Image & Video Audits
        </h2>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "16px" }}>
          <div style={{ padding: "14px", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
            <h4 style={{ fontSize: "0.92rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "6px" }}>
              1. 45-Degree Angle for Plates
            </h4>
            <p style={{ fontSize: "0.84rem", color: "var(--text-secondary)", lineHeight: 1.45 }}>
              Capture the full dish from a 45-degree angle or bird's-eye view so portion volume and side garnishes are visible.
            </p>
          </div>

          <div style={{ padding: "14px", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
            <h4 style={{ fontSize: "0.92rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "6px" }}>
              2. Natural Bright Lighting
            </h4>
            <p style={{ fontSize: "0.84rem", color: "var(--text-secondary)", lineHeight: 1.45 }}>
              Avoid harsh shadows and direct camera flash. Natural light reveals genuine food pigmentation and surface oxidation.
            </p>
          </div>

          <div style={{ padding: "14px", backgroundColor: "var(--bg-card-subtle)", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
            <h4 style={{ fontSize: "0.92rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "6px" }}>
              3. Steady Kitchen Video Panning
            </h4>
            <p style={{ fontSize: "0.84rem", color: "var(--text-secondary)", lineHeight: 1.45 }}>
              When taking a kitchen video, pan smoothly across counters and storage bins for 6 to 15 seconds to allow clean OpenCV keyframe capture.
            </p>
          </div>
        </div>
      </div>

      {/* Frequently Asked Questions */}
      <div className="card">
        <h2 style={{ fontSize: "1.2rem", fontWeight: 800, color: "var(--text-primary)", marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
          <BookOpen size={20} color="var(--brand-secondary)" /> Frequently Asked Questions
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {faqs.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <div
                key={idx}
                style={{
                  borderRadius: "var(--radius-sm)",
                  border: "1px solid var(--border-color)",
                  overflow: "hidden"
                }}
              >
                <button
                  onClick={() => setOpenFaq(isOpen ? null : idx)}
                  style={{
                    width: "100%",
                    padding: "14px 18px",
                    backgroundColor: isOpen ? "var(--bg-card-subtle)" : "var(--bg-card)",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    textAlign: "left",
                    color: "var(--text-primary)",
                    fontWeight: 700,
                    fontSize: "0.94rem"
                  }}
                >
                  <span>{faq.q}</span>
                  {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                </button>

                {isOpen && (
                  <div style={{ padding: "14px 18px", fontSize: "0.88rem", color: "var(--text-secondary)", lineHeight: 1.55, borderTop: "1px solid var(--border-color)" }}>
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
