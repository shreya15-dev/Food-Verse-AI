import cv2
import numpy as np
from PIL import Image
from services.ai_service import call_gemini_vision

DEMO_FRESHNESS_PROFILES = [
    {
        "category": "Looks fresh",
        "status_color": "success",
        "item_identified": "Fresh Crisp Produce",
        "freshness_score": 92,
        "confidence": 0.89,
        "observations": [
            {"cue": "Surface Pigmentation", "finding": "Vibrant and uniform natural skin coloration with no conspicuous browning."},
            {"cue": "Structural Integrity", "finding": "Firm, intact cellular epidermal structure without visible bruising or indentation."},
            {"cue": "Fungal/Mold Markers", "finding": "Zero detectable mycelial growth, velvety patches, or sporulation."},
            {"cue": "Moisture & Dehydration", "finding": "Healthy surface sheen; no signs of shriveling, wilting, or cellular collapse."}
        ],
        "shelf_life_estimate": "3 to 6 days under proper refrigeration (4°C / 40°F)",
        "recommendation": "Optimal for raw consumption or culinary use. Store in perforated crisper drawer.",
        "storage_tips": [
            "Keep dry before storing; moisture accelerates bacterial colonization.",
            "Store away from high-ethylene emitters like overripe bananas."
        ]
    },
    {
        "category": "Possible deterioration",
        "status_color": "warning",
        "item_identified": "Produce with Early Aging / Oxidation Signs",
        "freshness_score": 62,
        "confidence": 0.84,
        "observations": [
            {"cue": "Surface Pigmentation", "finding": "Mild enzymatic browning and localized discoloration spots detected."},
            {"cue": "Structural Integrity", "finding": "Slight loss of turgor pressure; localized softening or minor surface wrinkles."},
            {"cue": "Fungal/Mold Markers", "finding": "No macroscopic mold colonies present, but surface vulnerability is increased."},
            {"cue": "Moisture & Dehydration", "finding": "Marginal moisture depletion around edges or stems."}
        ],
        "shelf_life_estimate": "Consume within 24 to 48 hours",
        "recommendation": "Trim bruised outer areas. Best cooked thoroughly into soups, smoothies, or stir-fries rather than eaten raw.",
        "storage_tips": [
            "Use immediately or freeze in airtight containers for smoothies or stocks.",
            "Separate from fresh produce to prevent ethylene transfer."
        ]
    },
    {
        "category": "Uncertain / Spoilage detected",
        "status_color": "danger",
        "item_identified": "Suspect / Advanced Deterioration",
        "freshness_score": 34,
        "confidence": 0.91,
        "observations": [
            {"cue": "Surface Pigmentation", "finding": "Extensive dark lesions, patchy discoloration, and necrotic breakdown."},
            {"cue": "Structural Integrity", "finding": "Significant tissue collapse, mushiness, or compromised peel envelope."},
            {"cue": "Fungal/Mold Markers", "finding": "Suspicious surface patches resembling mold filaments or fungal colonies."},
            {"cue": "Moisture & Dehydration", "finding": "Evidence of weeping fluids or severe desiccation."}
        ],
        "shelf_life_estimate": "Expired / Compromised",
        "recommendation": "Do not consume. Discard or compost immediately to prevent cross-contamination.",
        "storage_tips": [
            "Clean and sanitize any containers or shelves where this item was stored.",
            "Wash hands thoroughly after handling deteriorated organic matter."
        ]
    }
]

def analyze_freshness(image_path: str, filename: str) -> dict:
    """
    Evaluates produce/food freshness through visual inspection.
    Uses Gemini Vision if configured, with a rich OpenCV-assisted fallback.
    """
    disclaimer = (
        "Strict Food Safety Notice: Visual cues cannot establish microbiological food safety. "
        "Harmful pathogens, bacterial toxins (e.g. Salmonella, Listeria, E. coli), and odorless spoilage "
        "cannot be detected by camera images. When in doubt, always discard questionable food."
    )

    # 1. Attempt Live Vision AI
    gemini_prompt = """
    Assess the freshness and condition of the food or produce visible in this image.
    Provide an objective, visual-only evaluation.
    Return a strictly formatted JSON object with:
    - item_identified: (string) food item observed
    - category: (string) choose exactly one from: 'Looks fresh', 'Possible deterioration', or 'Uncertain / Spoilage detected'
    - status_color: (string) 'success' for fresh, 'warning' for deterioration, 'danger' for spoilage
    - freshness_score: (integer 0-100)
    - confidence: (float 0.50 to 0.99)
    - observations: (array of objects with 'cue' and 'finding' keys) covering pigmentation, structural firmness, mold markers, and moisture
    - shelf_life_estimate: (string) estimated storage window
    - recommendation: (string) actionable food handling advice
    - storage_tips: (array of strings) 2 practical storage pointers
    """

    vision_res = call_gemini_vision(image_path, gemini_prompt)
    if vision_res.get("success"):
        data = vision_res["result"]
        data["is_demo"] = False
        data["analysis_mode"] = "Live Multimodal Vision AI (Gemini 1.5 Flash)"
        data["disclaimer"] = disclaimer
        return data

    # 2. OpenCV Visual Heuristic Fallback
    try:
        # Read image with OpenCV for image stats
        cv_img = cv2.imread(image_path)
        if cv_img is not None:
            # Check brightness and contrast
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
            # Brown/dark spots heuristic: low value and moderate saturation
            brown_mask = cv2.inRange(hsv, np.array([10, 50, 20]), np.array([30, 255, 120]))
            brown_ratio = np.sum(brown_mask > 0) / (cv_img.shape[0] * cv_img.shape[1])
        else:
            brown_ratio = 0.05
    except Exception:
        brown_ratio = 0.05

    fn_lower = filename.lower()
    if any(k in fn_lower for k in ["rot", "spoiled", "mold", "bad", "decay", "old"]) or brown_ratio > 0.25:
        chosen = DEMO_FRESHNESS_PROFILES[2] # Spoilage
    elif any(k in fn_lower for k in ["soft", "ripe", "brown", "aging", "wilt"]) or brown_ratio > 0.10:
        chosen = DEMO_FRESHNESS_PROFILES[1] # Deterioration
    else:
        chosen = DEMO_FRESHNESS_PROFILES[0] # Looks fresh

    res = dict(chosen)
    res["is_demo"] = True
    res["analysis_mode"] = "Heuristic Demo Simulation (No Vision API Key Detected)"
    res["disclaimer"] = disclaimer
    return res
