import React, { useState } from "react";
import { UtensilsCrossed, AlertCircle, Info, Sparkles, Printer } from "lucide-react";
import ImageUploader from "../components/ImageUploader";
import NutritionCard from "../components/NutritionCard";
import { analyzeFood } from "../services/api";
import { useToast } from "../components/Toast";

export default function FoodRecognition({ onScanCompleted }) {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();

  const presets = [
    { name: "Quinoa Bowl", emoji: "🥗", filename: "food_quinoa_salad.jpg", mediaUrl: "/sample_media/food_quinoa_salad.jpg" },
    { name: "Grilled Chicken", emoji: "🍗", filename: "food_grilled_chicken.jpg", mediaUrl: "/sample_media/food_grilled_chicken.jpg" },
    { name: "Margherita Pizza", emoji: "🍕", filename: "food_margherita_pizza.jpg", mediaUrl: "/sample_media/food_margherita_pizza.jpg" },
    { name: "Avocado Egg Toast", emoji: "🥑", filename: "avocado_poached_egg_toast.png" },
    { name: "Berry Acai Bowl", emoji: "🫐", filename: "berry_smoothie_bowl.png" },
    { name: "Paneer Tikka", emoji: "🧀", filename: "paneer_tikka_masala.png" }
  ];

  const handleSelectPreset = async (preset) => {
    if (preset.mediaUrl) {
      try {
        const response = await fetch(preset.mediaUrl);
        if (response.ok) {
          const blob = await response.blob();
          const file = new File([blob], preset.filename, { type: "image/jpeg" });
          handleUpload(file);
          return;
        }
      } catch (e) {
        // Fallback to canvas
      }
    }

    const canvas = document.createElement("canvas");
    canvas.width = 400;
    canvas.height = 300;
    const ctx = canvas.getContext("2d");
    
    ctx.fillStyle = preset.filename.includes("quinoa") ? "#4E7055" : preset.filename.includes("chicken") ? "#A77E58" : preset.filename.includes("pizza") ? "#C2410C" : preset.filename.includes("toast") ? "#65A30D" : preset.filename.includes("smoothie") ? "#7E22CE" : "#EA580C";
    ctx.fillRect(0, 0, 400, 300);

    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 22px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(preset.name, 200, 150);

    canvas.toBlob((blob) => {
      const file = new File([blob], preset.filename, { type: "image/png" });
      handleUpload(file);
    }, "image/png");
  };

  const handleUpload = async (file) => {
    setIsLoading(true);
    setAnalysisResult(null);

    const res = await analyzeFood(file);
    setIsLoading(false);

    if (res.success) {
      setAnalysisResult(res.data);
      addToast("Food analysis completed successfully!", "success");
      if (onScanCompleted) onScanCompleted();
    } else {
      addToast(res.error || "Failed to analyze food image.", "error");
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <UtensilsCrossed size={28} color="var(--brand-primary)" />
            AI Food Recognition & Nutrition
          </h1>
          <p className="page-description">
            Upload an image of a meal, snack, or beverage to detect food items, estimate portion sizes,
            compute calories and macronutrients, and view micronutrient composition.
          </p>
        </div>
      </div>

      {/* Main Upload Control */}
      <ImageUploader
        onUpload={handleUpload}
        isLoading={isLoading}
        loadingText="Analyzing ingredients & nutrition..."
        samplePresets={presets}
        onSelectPreset={handleSelectPreset}
      />

      {/* Results View */}
      {analysisResult && (
        <NutritionCard data={analysisResult} onPrint={handlePrint} />
      )}
    </div>
  );
}
