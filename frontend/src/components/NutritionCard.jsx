import React from "react";
import { Flame, Activity, ShieldAlert, Sparkles, Printer, CheckCircle, HeartPulse, Tag } from "lucide-react";

export default function NutritionCard({ data, onPrint }) {
  if (!data) return null;

  const {
    food_name = "Detected Food Item",
    category = "General Meal",
    serving_size = "1 serving",
    calories = 0,
    protein_g = 0,
    carbs_g = 0,
    fat_g = 0,
    fiber_g = 0,
    ingredients = [],
    vitamins = [],
    health_score = 80,
    dietary_tags = [],
    confidence = 0.85,
    is_demo = true,
    analysis_mode = "Simulation Mode",
    disclaimer = ""
  } = data;

  // Calculate approximate macro calorie contributions
  const proteinCals = protein_g * 4;
  const carbsCals = carbs_g * 4;
  const fatCals = fat_g * 9;
  const totalCalculatedCals = proteinCals + carbsCals + fatCals || 1;

  const proteinPct = Math.round((proteinCals / totalCalculatedCals) * 100);
  const carbsPct = Math.round((carbsCals / totalCalculatedCals) * 100);
  const fatPct = Math.round((fatCals / totalCalculatedCals) * 100);

  return (
    <div className="card" style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      {/* Top Title & Metadata Bar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "12px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            <span className="badge badge-neutral">{category}</span>
            <span className={`badge ${is_demo ? "badge-demo" : "badge-live"}`}>
              {is_demo ? <Sparkles size={12} /> : <CheckCircle size={12} />}
              {analysis_mode}
            </span>
            <span className="badge" style={{ backgroundColor: "var(--brand-light)", color: "var(--brand-primary)" }}>
              Confidence: {Math.round(confidence * 100)}%
            </span>
          </div>
          <h2 style={{ fontSize: "1.5rem", fontWeight: 800, marginTop: "8px", color: "var(--text-primary)" }}>
            {food_name}
          </h2>
          <span style={{ fontSize: "0.86rem", color: "var(--text-secondary)" }}>
            Serving reference: <strong>{serving_size}</strong>
          </span>
        </div>

        {onPrint && (
          <button onClick={onPrint} className="btn btn-outline" style={{ padding: "8px 14px", fontSize: "0.85rem" }}>
            <Printer size={15} /> Print Report
          </button>
        )}
      </div>

      {/* Hero Stats (Calories & Health Score) */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "14px"
        }}
      >
        {/* Calories Card */}
        <div
          style={{
            padding: "16px 20px",
            backgroundColor: "var(--bg-card-subtle)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--border-color)",
            display: "flex",
            alignItems: "center",
            gap: "16px"
          }}
        >
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              backgroundColor: "rgba(224, 122, 95, 0.15)",
              color: "var(--brand-accent)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center"
            }}
          >
            <Flame size={26} />
          </div>
          <div>
            <div style={{ fontSize: "1.75rem", fontWeight: 800, color: "var(--text-primary)", lineHeight: 1.1 }}>
              {calories}
            </div>
            <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase" }}>
              Estimated Calories (kcal)
            </span>
          </div>
        </div>

        {/* Health Score Card */}
        <div
          style={{
            padding: "16px 20px",
            backgroundColor: "var(--bg-card-subtle)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--border-color)",
            display: "flex",
            alignItems: "center",
            gap: "16px"
          }}
        >
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              backgroundColor: "rgba(45, 106, 79, 0.15)",
              color: "var(--brand-secondary)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center"
            }}
          >
            <HeartPulse size={26} />
          </div>
          <div>
            <div style={{ fontSize: "1.75rem", fontWeight: 800, color: "var(--brand-primary)", lineHeight: 1.1 }}>
              {health_score} <span style={{ fontSize: "0.95rem", fontWeight: 500, color: "var(--text-muted)" }}>/ 100</span>
            </div>
            <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase" }}>
              Nutritional Quality Index
            </span>
          </div>
        </div>
      </div>

      {/* Macronutrient Distribution Bars */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
          <h4 style={{ fontSize: "0.95rem", fontWeight: 700, color: "var(--text-primary)" }}>
            Macronutrient Breakdown
          </h4>
          <span style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
            % of estimated energy
          </span>
        </div>

        {/* Multi-colored composite progress bar */}
        <div
          style={{
            height: "14px",
            width: "100%",
            borderRadius: "999px",
            backgroundColor: "var(--bg-card-subtle)",
            display: "flex",
            overflow: "hidden",
            marginBottom: "16px"
          }}
        >
          <div style={{ width: `${proteinPct}%`, backgroundColor: "#2D6A4F" }} title={`Protein: ${proteinPct}%`} />
          <div style={{ width: `${carbsPct}%`, backgroundColor: "#E07A5F" }} title={`Carbs: ${carbsPct}%`} />
          <div style={{ width: `${fatPct}%`, backgroundColor: "#F4A261" }} title={`Fat: ${fatPct}%`} />
        </div>

        {/* Macro Metric Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))",
            gap: "12px"
          }}
        >
          <div style={{ padding: "12px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)", textAlign: "center" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", textTransform: "uppercase", fontWeight: 600 }}>
              Protein
            </span>
            <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#2D6A4F", marginTop: "2px" }}>
              {protein_g}g
            </div>
            <span style={{ fontSize: "0.72rem", color: "var(--text-secondary)" }}>{proteinPct}% energy</span>
          </div>

          <div style={{ padding: "12px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)", textAlign: "center" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", textTransform: "uppercase", fontWeight: 600 }}>
              Carbohydrates
            </span>
            <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#E07A5F", marginTop: "2px" }}>
              {carbs_g}g
            </div>
            <span style={{ fontSize: "0.72rem", color: "var(--text-secondary)" }}>{carbsPct}% energy</span>
          </div>

          <div style={{ padding: "12px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)", textAlign: "center" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", textTransform: "uppercase", fontWeight: 600 }}>
              Total Fats
            </span>
            <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#F4A261", marginTop: "2px" }}>
              {fat_g}g
            </div>
            <span style={{ fontSize: "0.72rem", color: "var(--text-secondary)" }}>{fatPct}% energy</span>
          </div>

          <div style={{ padding: "12px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)", textAlign: "center" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", textTransform: "uppercase", fontWeight: 600 }}>
              Dietary Fiber
            </span>
            <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "var(--brand-primary)", marginTop: "2px" }}>
              {fiber_g}g
            </div>
            <span style={{ fontSize: "0.72rem", color: "var(--text-secondary)" }}>Plant Roughage</span>
          </div>
        </div>
      </div>

      {/* Identified Ingredients & Dietary Tags */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "16px" }}>
        {ingredients && ingredients.length > 0 && (
          <div>
            <h4 style={{ fontSize: "0.9rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "8px" }}>
              Identified Ingredients & Components
            </h4>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
              {ingredients.map((ing, i) => (
                <span key={i} className="badge badge-neutral" style={{ fontSize: "0.8rem", padding: "5px 10px" }}>
                  {ing}
                </span>
              ))}
            </div>
          </div>
        )}

        {vitamins && vitamins.length > 0 && (
          <div>
            <h4 style={{ fontSize: "0.9rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "8px" }}>
              Micronutrients & Key Nutrients
            </h4>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
              {vitamins.map((vit, i) => (
                <span
                  key={i}
                  className="badge"
                  style={{
                    backgroundColor: "var(--brand-light)",
                    color: "var(--brand-primary)",
                    fontSize: "0.8rem",
                    padding: "5px 10px"
                  }}
                >
                  {vit}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Dietary Tags */}
      {dietary_tags && dietary_tags.length > 0 && (
        <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
          <Tag size={15} color="var(--text-muted)" />
          {dietary_tags.map((tag, idx) => (
            <span key={idx} className="badge badge-success" style={{ fontSize: "0.78rem" }}>
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Disclaimer Box */}
      {disclaimer && (
        <div className="disclaimer-box">
          <div style={{ display: "flex", alignItems: "center", gap: "6px", fontWeight: 600, marginBottom: "4px" }}>
            <ShieldAlert size={14} color="var(--brand-accent)" />
            <span>Important Nutritional Disclaimer</span>
          </div>
          <p>{disclaimer}</p>
        </div>
      )}
    </div>
  );
}
