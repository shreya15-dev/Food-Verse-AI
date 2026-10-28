import React, { useState } from "react";
import { ShieldCheck, Video, Eye, Info, Sparkles } from "lucide-react";
import ImageUploader from "../components/ImageUploader";
import HygieneAuditCard from "../components/HygieneAuditCard";
import { analyzeHygiene } from "../services/api";
import { useToast } from "../components/Toast";

export default function HygieneMonitor({ onScanCompleted }) {
  const [hygieneResult, setHygieneResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();

  const presets = [
    { name: "Walkthrough Video", emoji: "🎥", filename: "kitchen_audit_walkthrough.mp4", mediaUrl: "/sample_media/kitchen_audit_walkthrough.mp4", isVideo: true },
    { name: "Clean Station", emoji: "✨", filename: "kitchen_prep_clean.jpg", mediaUrl: "/sample_media/kitchen_prep_clean.jpg", color: "#1E3A8A" },
    { name: "Cluttered Counter", emoji: "⚠️", filename: "kitchen_prep_cluttered.jpg", mediaUrl: "/sample_media/kitchen_prep_cluttered.jpg", color: "#7F1D1D" }
  ];

  const handleSelectPreset = async (preset) => {
    if (preset.mediaUrl) {
      try {
        const response = await fetch(preset.mediaUrl);
        if (response.ok) {
          const blob = await response.blob();
          const mime = preset.isVideo ? "video/mp4" : "image/jpeg";
          const file = new File([blob], preset.filename, { type: mime });
          handleUpload(file);
          return;
        }
      } catch (e) {
        // Fallback to canvas
      }
    }

    // Canvas fallback
    const canvas = document.createElement("canvas");
    canvas.width = 480;
    canvas.height = 320;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = preset.color || "#1E293B";
    ctx.fillRect(0, 0, 480, 320);
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 20px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(preset.name, 240, 160);

    canvas.toBlob((blob) => {
      const file = new File([blob], preset.filename, { type: "image/png" });
      handleUpload(file);
    }, "image/png");
  };

  const handleUpload = async (file) => {
    setIsLoading(true);
    setHygieneResult(null);

    const res = await analyzeHygiene(file);
    setIsLoading(false);

    if (res.success) {
      setHygieneResult(res.data);
      addToast("Hygiene audit completed!", "success");
      if (onScanCompleted) onScanCompleted();
    } else {
      addToast(res.error || "Hygiene analysis failed.", "error");
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <ShieldCheck size={28} color="var(--brand-accent)" />
            Restaurant Hygiene Monitoring
          </h1>
          <p className="page-description">
            Audit commercial kitchen prep areas, stainless surfaces, open food containers, and potential
            cross-contamination hazards. Supports both kitchen photos and short video walkthroughs with OpenCV
            automated keyframe extraction.
          </p>
        </div>
      </div>

      <ImageUploader
        onUpload={handleUpload}
        isLoading={isLoading}
        loadingText="Processing media & extracting keyframes with OpenCV..."
        acceptVideo={true}
        samplePresets={presets}
        onSelectPreset={handleSelectPreset}
      />

      {hygieneResult && (
        <HygieneAuditCard data={hygieneResult} />
      )}
    </div>
  );
}
