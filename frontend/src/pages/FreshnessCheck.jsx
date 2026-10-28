import React, { useState } from "react";
import { Apple, ShieldAlert, Sparkles } from "lucide-react";
import ImageUploader from "../components/ImageUploader";
import FreshnessMeter from "../components/FreshnessMeter";
import { analyzeFreshness } from "../services/api";
import { useToast } from "../components/Toast";

export default function FreshnessCheck({ onScanCompleted }) {
  const [freshnessResult, setFreshnessResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();

  const presets = [
    { name: "Crisp Fresh Apple", emoji: "🍎", filename: "fresh_crisp_apple.jpg", mediaUrl: "/sample_media/fresh_crisp_apple.jpg", color: "#DC2626" },
    { name: "Vibrant Greens", emoji: "🥬", filename: "fresh_salad_greens.png", color: "#16A34A" },
    { name: "Aging Browning Fruit", emoji: "🍌", filename: "aging_ripe_banana.png", color: "#CA8A04" },
    { name: "Compromised / Spoiled", emoji: "⚠️", filename: "produce_browning_decay.jpg", mediaUrl: "/sample_media/produce_browning_decay.jpg", color: "#78350F" }
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

    ctx.fillStyle = preset.color || "#2D6A4F";
    ctx.fillRect(0, 0, 400, 300);

    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 20px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(preset.name, 200, 150);

    canvas.toBlob((blob) => {
      const file = new File([blob], preset.filename, { type: "image/png" });
      handleUpload(file);
    }, "image/png");
  };

  const handleUpload = async (file) => {
    setIsLoading(true);
    setFreshnessResult(null);

    const res = await analyzeFreshness(file);
    setIsLoading(false);

    if (res.success) {
      setFreshnessResult(res.data);
      addToast("Freshness evaluation complete!", "success");
      if (onScanCompleted) onScanCompleted();
    } else {
      addToast(res.error || "Failed to analyze produce freshness.", "error");
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <Apple size={28} color="var(--brand-secondary)" />
            Food Freshness Assessment
          </h1>
          <p className="page-description">
            Inspect fruits, vegetables, and pantry staples for observable signs of deterioration,
            enzymatic browning, surface texture softening, and fungal indicators.
          </p>
        </div>
      </div>

      <ImageUploader
        onUpload={handleUpload}
        isLoading={isLoading}
        loadingText="Evaluating surface condition & oxidation..."
        samplePresets={presets}
        onSelectPreset={handleSelectPreset}
      />

      {freshnessResult && (
        <FreshnessMeter data={freshnessResult} />
      )}
    </div>
  );
}
