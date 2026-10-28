import React, { useState, useEffect } from "react";
import {
  CalendarHeart,
  Flame,
  Activity,
  ShoppingCart,
  Printer,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Clock,
  Check,
  ChevronRight,
  ShieldAlert,
  Loader2
} from "lucide-react";
import { generateMealPlan, getSavedMealPlan } from "../services/api";
import { useToast } from "../components/Toast";

export default function MealPlanner() {
  const [profile, setProfile] = useState({
    age: 26,
    gender: "male",
    height_cm: 175,
    weight_kg: 70,
    activity_level: "moderately_active",
    dietary_preference: "Balanced",
    goal: "maintain",
    meal_frequency: "3_meals_1_snack",
    allergies: [],
    disliked_ingredients: []
  });

  const [activeDayIndex, setActiveDayIndex] = useState(0);
  const [planResult, setPlanResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [checkedGrocery, setCheckedGrocery] = useState({});
  const { addToast } = useToast();

  const allergyOptions = ["Peanuts", "Tree Nuts", "Dairy", "Gluten", "Eggs", "Shellfish", "Soy"];

  useEffect(() => {
    // Attempt loading last saved plan on initial render
    const loadSaved = async () => {
      const res = await getSavedMealPlan();
      if (res?.success && res?.data?.saved_plan) {
        setPlanResult(res.data.saved_plan.plan);
        if (res.data.profile) setProfile(res.data.profile);
      }
    };
    loadSaved();
  }, []);

  const handleProfileChange = (field, value) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  const toggleAllergy = (allergy) => {
    setProfile((prev) => {
      const exists = prev.allergies.includes(allergy);
      return {
        ...prev,
        allergies: exists ? prev.allergies.filter((a) => a !== allergy) : [...prev.allergies, allergy]
      };
    });
  };

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    setIsLoading(true);

    const res = await generateMealPlan(profile);
    setIsLoading(false);

    if (res.success && res.data) {
      setPlanResult(res.data);
      addToast("7-Day personalized meal plan generated!", "success");
    } else {
      addToast(res.error || "Failed to generate meal plan.", "error");
    }
  };

  const toggleGroceryItem = (item) => {
    setCheckedGrocery((prev) => ({ ...prev, [item]: !prev[item] }));
  };

  const handlePrint = () => {
    window.print();
  };

  const currentDay = planResult?.schedule?.[activeDayIndex];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "28px" }}>
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <CalendarHeart size={28} color="#E76F51" />
            Personalized Nutrition & 7-Day Meal Planner
          </h1>
          <p className="page-description">
            Scientifically computed calorie and macronutrient distributions based on the Mifflin-St Jeor
            equation. Generate adaptable weekly meal schedules and aggregated grocery lists tailored to your lifestyle.
          </p>
        </div>

        {planResult && (
          <button onClick={handlePrint} className="btn btn-outline">
            <Printer size={16} /> Print Full Plan
          </button>
        )}
      </div>

      {/* Profile Setup Form */}
      <div className="card">
        <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "18px" }}>
          Nutritional Profile & Health Parameters
        </h3>

        <form onSubmit={handleGenerate} style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          {/* Row 1: Age, Gender, Height, Weight */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "14px" }}>
            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Age (years)
              </label>
              <input
                type="number"
                min="14"
                max="100"
                value={profile.age}
                onChange={(e) => handleProfileChange("age", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
                required
              />
            </div>

            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Biological Gender
              </label>
              <select
                value={profile.gender}
                onChange={(e) => handleProfileChange("gender", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Non-binary / Other</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Height (cm)
              </label>
              <input
                type="number"
                min="120"
                max="230"
                value={profile.height_cm}
                onChange={(e) => handleProfileChange("height_cm", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
                required
              />
            </div>

            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Weight (kg)
              </label>
              <input
                type="number"
                min="35"
                max="250"
                value={profile.weight_kg}
                onChange={(e) => handleProfileChange("weight_kg", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
                required
              />
            </div>
          </div>

          {/* Row 2: Activity, Dietary Preference, Primary Goal */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "14px" }}>
            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Activity Level
              </label>
              <select
                value={profile.activity_level}
                onChange={(e) => handleProfileChange("activity_level", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
              >
                <option value="sedentary">Sedentary (Desk job, minimal exercise)</option>
                <option value="lightly_active">Lightly Active (1–3 exercise days/wk)</option>
                <option value="moderately_active">Moderately Active (3–5 exercise days/wk)</option>
                <option value="very_active">Very Active (6–7 intense training days/wk)</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Dietary Framework
              </label>
              <select
                value={profile.dietary_preference}
                onChange={(e) => handleProfileChange("dietary_preference", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
              >
                <option value="Balanced">Balanced Omnivore</option>
                <option value="Vegetarian">Vegetarian (Lacto-Ovo)</option>
                <option value="Vegan">100% Plant-Based Vegan</option>
                <option value="Pescatarian">Pescatarian (Fish + Veg)</option>
                <option value="Keto">Ketogenic (Low-Carb, High-Fat)</option>
                <option value="High_Protein">High-Protein Fitness</option>
              </select>
            </div>

            <div>
              <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
                Health & Body Goal
              </label>
              <select
                value={profile.goal}
                onChange={(e) => handleProfileChange("goal", e.target.value)}
                style={{ width: "100%", marginTop: "4px" }}
              >
                <option value="maintain">Weight Maintenance & Vitality</option>
                <option value="healthy_weight_loss">Healthy Weight Loss (-350 kcal/day)</option>
                <option value="lean_muscle_gain">Lean Muscle Gain (+350 kcal/day)</option>
              </select>
            </div>
          </div>

          {/* Allergies / Exclusions */}
          <div>
            <label style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)", display: "block", marginBottom: "6px" }}>
              Food Allergies & Exclusions
            </label>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
              {allergyOptions.map((al) => {
                const checked = profile.allergies.includes(al);
                return (
                  <button
                    key={al}
                    type="button"
                    onClick={() => toggleAllergy(al)}
                    className={`badge ${checked ? "badge-danger" : "badge-neutral"}`}
                    style={{ cursor: "pointer", padding: "6px 12px", border: "1px solid var(--border-color)" }}
                  >
                    {checked ? `✓ No ${al}` : al}
                  </button>
                );
              })}
            </div>
          </div>

          <div style={{ display: "flex", justifyContent: "flex-end", marginTop: "8px" }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isLoading}
              style={{ minWidth: "180px", padding: "12px 24px" }}
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="spin-icon" style={{ animation: "spin 1s linear infinite" }} />
                  Computing Diet Plan...
                </>
              ) : (
                <>
                  <Sparkles size={16} /> Generate 7-Day Plan
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Generated Energy Targets & Macro Splits */}
      {planResult && (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: "14px"
            }}
          >
            <div className="card" style={{ padding: "18px" }}>
              <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
                Target Daily Energy
              </span>
              <div style={{ fontSize: "1.75rem", fontWeight: 900, color: "var(--brand-primary)", marginTop: "4px" }}>
                {planResult.targets.target_calories} <span style={{ fontSize: "0.9rem", color: "var(--text-muted)", fontWeight: 500 }}>kcal</span>
              </div>
              <span style={{ fontSize: "0.76rem", color: "var(--text-secondary)" }}>
                BMR: {planResult.targets.bmr} | TDEE: {planResult.targets.tdee}
              </span>
            </div>

            <div className="card" style={{ padding: "18px" }}>
              <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
                Daily Protein Goal
              </span>
              <div style={{ fontSize: "1.75rem", fontWeight: 900, color: "#2D6A4F", marginTop: "4px" }}>
                {planResult.targets.target_protein_g}g
              </div>
              <span style={{ fontSize: "0.76rem", color: "var(--text-secondary)" }}>
                {planResult.targets.macro_split_percentages.protein}% of daily calories
              </span>
            </div>

            <div className="card" style={{ padding: "18px" }}>
              <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
                Daily Carbohydrates
              </span>
              <div style={{ fontSize: "1.75rem", fontWeight: 900, color: "#E07A5F", marginTop: "4px" }}>
                {planResult.targets.target_carbs_g}g
              </div>
              <span style={{ fontSize: "0.76rem", color: "var(--text-secondary)" }}>
                {planResult.targets.macro_split_percentages.carbs}% of daily calories
              </span>
            </div>

            <div className="card" style={{ padding: "18px" }}>
              <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
                Daily Healthy Fats
              </span>
              <div style={{ fontSize: "1.75rem", fontWeight: 900, color: "#F4A261", marginTop: "4px" }}>
                {planResult.targets.target_fat_g}g
              </div>
              <span style={{ fontSize: "0.76rem", color: "var(--text-secondary)" }}>
                {planResult.targets.macro_split_percentages.fat}% of daily calories
              </span>
            </div>
          </div>

          {/* 7-Day Day Selector Tabs */}
          <div className="card" style={{ padding: "20px" }}>
            <div style={{ display: "flex", gap: "8px", overflowX: "auto", paddingBottom: "12px", borderBottom: "1px solid var(--border-color)" }}>
              {planResult.schedule.map((day, idx) => {
                const isActive = activeDayIndex === idx;
                return (
                  <button
                    key={day.day}
                    onClick={() => setActiveDayIndex(idx)}
                    className={`btn ${isActive ? "btn-primary" : "btn-outline"}`}
                    style={{ padding: "8px 16px", borderRadius: "999px", fontSize: "0.88rem", whiteSpace: "nowrap" }}
                  >
                    {day.day}
                  </button>
                );
              })}
            </div>

            {/* Current Day Meal Schedule */}
            {currentDay && (
              <div style={{ marginTop: "20px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "10px" }}>
                  <h3 style={{ fontSize: "1.25rem", fontWeight: 800, color: "var(--text-primary)" }}>
                    {currentDay.day} Schedule
                  </h3>
                  <div style={{ display: "flex", gap: "12px", fontSize: "0.85rem", color: "var(--text-secondary)" }}>
                    <span>Total: <strong>{currentDay.daily_totals.calories} kcal</strong></span>
                    <span>•</span>
                    <span>P: <strong>{currentDay.daily_totals.protein_g}g</strong></span>
                    <span>C: <strong>{currentDay.daily_totals.carbs_g}g</strong></span>
                    <span>F: <strong>{currentDay.daily_totals.fat_g}g</strong></span>
                  </div>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px" }}>
                  {currentDay.meals.map((meal, mIdx) => (
                    <div
                      key={mIdx}
                      style={{
                        padding: "16px",
                        borderRadius: "var(--radius-md)",
                        backgroundColor: "var(--bg-card-subtle)",
                        border: "1px solid var(--border-color)",
                        display: "flex",
                        flexDirection: "column",
                        gap: "8px"
                      }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span className="badge badge-neutral" style={{ fontWeight: 700 }}>
                          {meal.type}
                        </span>
                        <span style={{ fontSize: "0.78rem", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "4px" }}>
                          <Clock size={12} /> {meal.prep_time}
                        </span>
                      </div>

                      <h4 style={{ fontSize: "0.98rem", fontWeight: 700, color: "var(--text-primary)" }}>
                        {meal.name}
                      </h4>

                      <div style={{ display: "flex", gap: "8px", fontSize: "0.8rem", color: "var(--brand-primary)", fontWeight: 600 }}>
                        <span>{meal.calories} kcal</span>
                        <span>•</span>
                        <span>{meal.protein_g}g P</span>
                        <span>•</span>
                        <span>{meal.carbs_g}g C</span>
                        <span>•</span>
                        <span>{meal.fat_g}g F</span>
                      </div>

                      <div style={{ fontSize: "0.78rem", color: "var(--text-secondary)", marginTop: "4px" }}>
                        <strong>Ingredients:</strong> {meal.ingredients.join(", ")}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Unified 7-Day Grocery List */}
          <div className="card">
            <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
              <div
                style={{
                  width: "38px",
                  height: "38px",
                  borderRadius: "var(--radius-sm)",
                  backgroundColor: "var(--brand-light)",
                  color: "var(--brand-primary)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center"
                }}
              >
                <ShoppingCart size={20} />
              </div>
              <div>
                <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "var(--text-primary)" }}>
                  Consolidated Weekly Grocery Checklist
                </h3>
                <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                  Aggregated across all 7 days of your personalized schedule
                </span>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "20px" }}>
              {Object.entries(planResult.grocery_list).map(([category, items]) => (
                <div
                  key={category}
                  style={{
                    padding: "16px",
                    borderRadius: "var(--radius-md)",
                    backgroundColor: "var(--bg-card-subtle)",
                    border: "1px solid var(--border-color)"
                  }}
                >
                  <h4 style={{ fontSize: "0.92rem", fontWeight: 700, color: "var(--brand-primary)", marginBottom: "10px" }}>
                    {category} ({items.length})
                  </h4>
                  <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                    {items.map((item, idx) => {
                      const isChecked = !!checkedGrocery[item];
                      return (
                        <label
                          key={idx}
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                            fontSize: "0.86rem",
                            cursor: "pointer",
                            textDecoration: isChecked ? "line-through" : "none",
                            color: isChecked ? "var(--text-muted)" : "var(--text-primary)"
                          }}
                        >
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={() => toggleGroceryItem(item)}
                            style={{ cursor: "pointer", width: "16px", height: "16px" }}
                          />
                          <span>{item}</span>
                        </label>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Substitutions & Medical Disclaimer */}
          <div className="disclaimer-box">
            <div style={{ display: "flex", alignItems: "center", gap: "6px", fontWeight: 700, marginBottom: "4px" }}>
              <ShieldAlert size={16} color="var(--brand-accent)" /> Educational Nutrition Disclaimer
            </div>
            <p>{planResult.disclaimer}</p>
          </div>
        </>
      )}
    </div>
  );
}
