import React, { useState, useRef } from "react";
import { UploadCloud, Image as ImageIcon, Video, X, Check, AlertCircle, Loader2, Sparkles } from "lucide-react";

export default function ImageUploader({
  onUpload,
  isLoading,
  loadingText = "Analyzing media...",
  acceptVideo = false,
  samplePresets = [],
  onSelectPreset
}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [validationError, setValidationError] = useState("");
  const fileInputRef = useRef(null);

  const allowedImageTypes = ["image/jpeg", "image/png", "image/webp", "image/jpg"];
  const allowedVideoTypes = ["video/mp4", "video/webm", "video/quicktime"];

  const handleFile = (file) => {
    setValidationError("");
    if (!file) return;

    const ext = file.name ? file.name.split('.').pop().toLowerCase() : '';
    const isVideo = (file.type && file.type.startsWith("video/")) || allowedVideoTypes.includes(file.type) || ['mp4', 'webm', 'mov', 'avi'].includes(ext);
    const isImage = (file.type && file.type.startsWith("image/")) || allowedImageTypes.includes(file.type) || ['jpg', 'jpeg', 'png', 'webp'].includes(ext);

    if (acceptVideo && !isImage && !isVideo) {
      setValidationError("Invalid file type. Please upload a JPG, PNG, WEBP image or MP4, WEBM video.");
      return;
    }
    if (!acceptVideo && !isImage) {
      setValidationError("Invalid file type. Supported formats: JPG, JPEG, PNG, and WEBP.");
      return;
    }

    // Size limit check
    const maxLimitBytes = isVideo ? 35 * 1024 * 1024 : 15 * 1024 * 1024;
    const maxLimitMb = isVideo ? 35 : 15;
    if (file.size > maxLimitBytes) {
      setValidationError(`File is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum allowed is ${maxLimitMb} MB.`);
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleClear = () => {
    if (previewUrl && previewUrl.startsWith("blob:")) URL.revokeObjectURL(previewUrl);
    setSelectedFile(null);
    setPreviewUrl(null);
    setValidationError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handlePresetClick = (preset) => {
    if (isLoading) return;
    if (preset.mediaUrl) {
      setPreviewUrl(preset.mediaUrl);
      setSelectedFile({
        name: preset.filename,
        size: preset.isVideo ? 1800000 : 350000,
        type: preset.isVideo ? "video/mp4" : "image/jpeg"
      });
    }
    if (onSelectPreset) {
      onSelectPreset(preset);
    }
  };

  const handleSubmit = () => {
    if (selectedFile && onUpload) {
      onUpload(selectedFile);
    }
  };

  const isVideoFile = selectedFile?.type?.startsWith("video/") || selectedFile?.name?.toLowerCase().endsWith(".mp4");

  return (
    <div style={{ width: "100%", marginBottom: "24px" }}>
      {/* Upload Zone */}
      {!selectedFile ? (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: `2px dashed ${isDragOver ? "var(--brand-primary)" : "var(--border-color)"}`,
            backgroundColor: isDragOver ? "var(--brand-light)" : "var(--bg-card)",
            borderRadius: "var(--radius-lg)",
            padding: "40px 24px",
            textAlign: "center",
            cursor: "pointer",
            transition: "var(--transition)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "12px",
            boxShadow: isDragOver ? "var(--shadow-md)" : "none"
          }}
        >
          <div
            style={{
              width: "60px",
              height: "60px",
              borderRadius: "50%",
              backgroundColor: "var(--brand-light)",
              color: "var(--brand-primary)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center"
            }}
          >
            {acceptVideo ? <Video size={28} /> : <UploadCloud size={30} />}
          </div>

          <div>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-primary)" }}>
              Drag & Drop your {acceptVideo ? "food photo or kitchen video" : "food image"} here
            </h3>
            <p style={{ fontSize: "0.86rem", color: "var(--text-secondary)", marginTop: "4px" }}>
              or <span style={{ color: "var(--brand-accent)", fontWeight: 600, textDecoration: "underline" }}>browse files</span> from your computer
            </p>
          </div>

          <div style={{ fontSize: "0.78rem", color: "var(--text-muted)", display: "flex", gap: "12px", flexWrap: "wrap", justifyContent: "center" }}>
            <span>Supports JPG, JPEG, PNG, WEBP {acceptVideo ? "• MP4, WEBM" : ""}</span>
            <span>•</span>
            <span>Max {acceptVideo ? "35 MB" : "15 MB"}</span>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept={acceptVideo ? "image/jpeg,image/png,image/webp,video/mp4,video/webm" : "image/jpeg,image/png,image/webp"}
            style={{ display: "none" }}
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                handleFile(e.target.files[0]);
              }
            }}
          />
        </div>
      ) : (
        /* Preview & Action Panel */
        <div
          className="card"
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "16px",
            padding: "20px"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <div
                style={{
                  width: "44px",
                  height: "44px",
                  borderRadius: "var(--radius-sm)",
                  backgroundColor: "var(--brand-light)",
                  color: "var(--brand-primary)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0
                }}
              >
                {isVideoFile ? <Video size={22} /> : <ImageIcon size={22} />}
              </div>
              <div>
                <h4 style={{ fontSize: "0.96rem", fontWeight: 700, wordBreak: "break-all" }}>
                  {selectedFile.name}
                </h4>
                <span style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
                  {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type || "file"}
                </span>
              </div>
            </div>

            <button
              onClick={handleClear}
              className="btn btn-outline"
              style={{ padding: "6px 12px", fontSize: "0.82rem" }}
              disabled={isLoading}
              title="Remove file"
            >
              <X size={15} /> Remove
            </button>
          </div>

          {/* Media Preview Box */}
          <div
            style={{
              maxHeight: "320px",
              backgroundColor: "var(--bg-card-subtle)",
              borderRadius: "var(--radius-md)",
              overflow: "hidden",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: "1px solid var(--border-color)"
            }}
          >
            {isVideoFile ? (
              <video
                src={previewUrl}
                controls
                style={{ maxHeight: "300px", maxWidth: "100%", objectFit: "contain" }}
              />
            ) : (
              <img
                src={previewUrl}
                alt="Upload preview"
                style={{ maxHeight: "300px", maxWidth: "100%", objectFit: "contain" }}
              />
            )}
          </div>

          {/* Submit Action */}
          <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
            <button
              onClick={handleSubmit}
              className="btn btn-primary"
              disabled={isLoading}
              style={{ minWidth: "160px" }}
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="spin-icon" style={{ animation: "spin 1s linear infinite" }} />
                  {loadingText}
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  Analyze Now
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Validation Error Message */}
      {validationError && (
        <div
          style={{
            marginTop: "12px",
            padding: "10px 14px",
            backgroundColor: "var(--status-danger-bg)",
            color: "var(--status-danger)",
            borderRadius: "var(--radius-sm)",
            fontSize: "0.86rem",
            display: "flex",
            alignItems: "center",
            gap: "8px"
          }}
        >
          <AlertCircle size={16} />
          <span>{validationError}</span>
        </div>
      )}

      {/* Sample presets for fast testing */}
      {samplePresets && samplePresets.length > 0 && !selectedFile && (
        <div style={{ marginTop: "16px", display: "flex", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
          <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-secondary)" }}>
            Quick Demo Presets:
          </span>
          {samplePresets.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => onSelectPreset && onSelectPreset(preset)}
              className="badge badge-neutral"
              style={{
                cursor: "pointer",
                padding: "6px 12px",
                border: "1px solid var(--border-color)",
                transition: "var(--transition)"
              }}
              title={`Load sample ${preset.name}`}
            >
              <span>{preset.emoji || "🍽️"}</span> {preset.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
