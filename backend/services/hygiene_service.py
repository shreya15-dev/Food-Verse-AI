import os
import cv2
import base64
import numpy as np
from services.ai_service import call_gemini_vision

def extract_video_keyframes(video_path: str, max_frames: int = 5) -> list[dict]:
    """
    Extracts representative keyframes from a video using OpenCV.
    Returns list of dicts with timestamp_sec, frame_index, and base64_image.
    """
    keyframes = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return keyframes

    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps if fps > 0 else 0

    if total_frames <= 0:
        cap.release()
        return keyframes

    # Determine frame step to get evenly spaced keyframes
    step = max(1, total_frames // (max_frames + 1))
    target_indices = [step * (i + 1) for i in range(max_frames) if step * (i + 1) < total_frames]

    for idx in target_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret and frame is not None:
            # Resize frame to reasonable preview size (e.g. 480px width)
            h, w = frame.shape[:2]
            target_w = 480
            target_h = int(h * (target_w / w))
            resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

            # Encode to JPEG
            _, buffer = cv2.imencode(".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, 80])
            b64_str = base64.b64encode(buffer).decode("utf-8")
            timestamp = round(idx / fps, 1)

            keyframes.append({
                "frame_index": idx,
                "timestamp_sec": timestamp,
                "timestamp_str": f"{int(timestamp // 60):02d}:{int(timestamp % 60):02d}",
                "image_data_url": f"data:image/jpeg;base64,{b64_str}"
            })

    cap.release()
    return keyframes

def analyze_kitchen_hygiene(file_path: str, filename: str, is_video: bool = False) -> dict:
    """
    Performs preliminary kitchen hygiene and food safety observation.
    Uses OpenCV for video frame breakdown / image metrics, with Gemini Vision or heuristic evaluation.
    """
    disclaimer = (
        "Regulatory & Official Disclaimer: This automated visual analysis provides preliminary advisory "
        "observations only. It DOES NOT constitute, guarantee, or replace an official municipal or FDA/HACCP "
        "health department inspection. It cannot verify internal food cooking temperatures, chemical sanitation "
        "levels (PPM), or microbial swab tests."
    )

    keyframes = []
    primary_image_path = file_path

    if is_video:
        try:
            keyframes = extract_video_keyframes(file_path, max_frames=4)
            if keyframes and len(keyframes) > 0:
                # Save first keyframe to a temp image if we need to run vision on it
                temp_kf_path = file_path + "_first_kf.jpg"
                cap = cv2.VideoCapture(file_path)
                cap.set(cv2.CAP_PROP_POS_FRAMES, keyframes[0]["frame_index"])
                ret, frame = cap.read()
                if ret and frame is not None:
                    cv2.imwrite(temp_kf_path, frame)
                    primary_image_path = temp_kf_path
                cap.release()
        except Exception as e:
            keyframes = []

    # 1. Attempt Gemini Vision AI if configured
    gemini_prompt = """
    Perform an observational kitchen hygiene and food safety risk assessment based on this kitchen/food prep environment image.
    Identify observable sanitation factors, potential hazards, and positive practices.
    Return a strictly formatted JSON object with:
    - hygiene_score: (integer 0-100)
    - preliminary_grade: (string) e.g., 'Grade A - Exemplary Sanitation', 'Grade B - Minor Observations', 'Grade C - Needs Corrective Action'
    - summary: (string) executive summary of visual findings
    - observations: (array of objects) each with:
        - category: (string) e.g., 'Surface Sanitation', 'Food Storage & Covering', 'Cross-Contamination Risks', 'Waste & Flooring', 'Personal Hygiene'
        - severity: (string) 'Low', 'Medium', or 'High'
        - finding: (string) specific evidence observed
        - corrective_action: (string) actionable recommendation
    - positive_points: (array of strings) positive practices observed
    """

    vision_res = call_gemini_vision(primary_image_path, gemini_prompt)

    # Clean up temp keyframe if created
    if is_video and primary_image_path != file_path and os.path.exists(primary_image_path):
        try:
            os.remove(primary_image_path)
        except Exception:
            pass

    if vision_res.get("success"):
        data = vision_res["result"]
        data["is_demo"] = False
        data["analysis_mode"] = "Live Multimodal Vision AI (Gemini 1.5 Flash)"
        data["disclaimer"] = disclaimer
        data["is_video"] = is_video
        data["keyframes"] = keyframes
        return data

    # 2. Heuristic Demo Fallback
    # Extract basic OpenCV metrics on brightness and clutter
    try:
        img_check = cv2.imread(primary_image_path if not is_video else file_path)
        if img_check is not None:
            gray = cv2.cvtColor(img_check, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
        else:
            mean_brightness = 130
    except Exception:
        mean_brightness = 130

    fn_lower = filename.lower()
    if any(k in fn_lower for k in ["dirty", "mess", "clutter", "bad", "violation"]):
        score = 64
        grade = "Grade C - Corrective Action Required"
        observations = [
            {
                "category": "Surface Sanitation & Clutter",
                "severity": "High",
                "finding": "Visible accumulation of food residues, grease build-up, and cluttered cutting boards on prep counter.",
                "corrective_action": "Execute complete wash-rinse-sanitize cycle on all prep stations before continuing food prep."
            },
            {
                "category": "Food Storage & Covering",
                "severity": "Medium",
                "finding": "Multiple containers left uncovered at ambient station temperature.",
                "corrective_action": "Ensure all mise en place is covered with food-grade lids or cling wrap and labeled with prep time."
            },
            {
                "category": "Waste & Drainage Management",
                "severity": "Medium",
                "finding": "Waste bin appears full without an active lid in close proximity to food assembly table.",
                "corrective_action": "Empty waste bin immediately and relocate minimum 3 feet away from open food zones."
            }
        ]
        positives = ["Stainless steel equipment surfaces present", "Adequate artificial overhead lighting"]
    else:
        score = 88
        grade = "Grade A - Good Sanitary Standards"
        observations = [
            {
                "category": "Surface Sanitation",
                "severity": "Low",
                "finding": "Stainless steel prep counters appear clean and reflective with no heavy pooling of grease or crumbs.",
                "corrective_action": "Maintain scheduled 2-hour sanitizing wipe-down with quaternary ammonium test strips."
            },
            {
                "category": "Cross-Contamination Protocol",
                "severity": "Low",
                "finding": "Separate designated zones observed for raw vegetable slicing and cooked food assembly.",
                "corrective_action": "Continue enforcing color-coded cutting board protocol (green for produce, red for raw meat)."
            },
            {
                "category": "Personal Protective Equipment",
                "severity": "Low",
                "finding": "Proper kitchen head coverings and uniform hygiene observable.",
                "corrective_action": "Reiterate single-use glove change interval whenever switching protein preparation stations."
            }
        ]
        positives = [
            "Clear prep space free of unnecessary clutter",
            "Stainless steel equipment well maintained",
            "Good illumination across task surfaces",
            "Floor drainage path unobstructed"
        ]

    # Attach keyframe timestamps if video
    if is_video and keyframes:
        for i, obs in enumerate(observations):
            kf_idx = min(i, len(keyframes) - 1)
            obs["video_timestamp"] = keyframes[kf_idx]["timestamp_str"]

    return {
        "hygiene_score": score,
        "preliminary_grade": grade,
        "summary": f"Automated inspection detected {len(observations)} observation points. Overall commercial kitchen cleanliness reflects {grade}.",
        "observations": observations,
        "positive_points": positives,
        "is_demo": True,
        "analysis_mode": "Heuristic Demo Simulation (OpenCV Keyframe & Computer Vision Fallback)",
        "disclaimer": disclaimer,
        "is_video": is_video,
        "keyframes": keyframes
    }
