# Academic Capstone Project Report: Food Verse AI 🥗

**Project Title:** Food Verse AI: A Multimodal Artificial Intelligence Platform for Dietary Nutrition Estimation, Produce Freshness Assessment, and Commercial Kitchen Hygiene Auditing  
**Tagline:** *"Smarter Food Choices. Safer Kitchens. Healthier Living."*  
**Date:** October 2026  
**Status:** Submission-Ready & Fully Functional  

---

## 1. Abstract & Executive Summary

Modern urban lifestyles and institutional food operations encounter significant blind spots in food intelligence: nutritional opacity in prepared meals, premature disposal of cosmetically imperfect yet consumable produce, and operational oversights in commercial prep kitchens. 

**Food Verse AI** is a multimodal full-stack web application developed to bridge these gaps. Combining computer vision, digital image and video processing, conversational artificial intelligence, and clinical dietary modeling, the platform delivers five core modules:
1. **AI Food Recognition & Nutrition Estimation**: Computes caloric and macronutrient values from plate photographs.
2. **Food Freshness Assessment**: Identifies enzymatic browning, epidermal loss of turgor, and fungal colonization cues to provide usable shelf-life estimates and discard recommendations.
3. **Restaurant Hygiene Monitoring**: Processes kitchen photographs and MP4/WEBM video walkthroughs via OpenCV keyframe extraction to flag sanitation risks and cross-contamination hazards.
4. **Smart Cooking Assistant**: Conversational recipe generation with pantry ingredient matching, dietary constraint filtering, and smart culinary substitutions.
5. **Personalized Nutrition & 7-Day Meal Planner**: Calculates Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the clinically validated Mifflin-St Jeor formula, outputting a complete weekly meal schedule and consolidated grocery checklist.

Crucially, the system features an honest, zero-credential heuristic fallback engine that functions 100% offline while offering plug-and-play multimodal vision support via Google Gemini 1.5 Flash.

---

## 2. Problem Statement & Objectives

### Problem Statement
- **Nutritional Inaccuracy**: Consumers struggle to estimate portion sizes, hidden fats, and caloric density of home-cooked and restaurant meals.
- **Produce Waste & Spoilage**: Millions of tons of edible produce are discarded prematurely due to minor oxidation, while dangerous spoilage is sometimes overlooked.
- **Commercial Sanitation Oversight**: Maintaining continuous compliance with HACCP / health regulations is challenging without objective visual auditing tools.

### Objectives
1. Build an intuitive, responsive SaaS web interface adhering to modern UI/UX design standards without third-party paid component libraries.
2. Develop a Python Flask REST backend with secure temporary file handling and CORS support.
3. Integrate OpenCV (`cv2`) for automated video frame extraction and image analysis.
4. Persist scan history and meal plans in a local SQLite database.
5. Provide transparent AI labeling distinguishing genuine multimodal AI inferences from heuristic simulations.

---

## 3. System Architecture & Technical Stack

```
                          ┌────────────────────────┐
                          │   React 19 Frontend    │
                          │   (Vite + Lucide Icons)│
                          └───────────┬────────────┘
                                      │ HTTP / REST
                                      ▼
                          ┌────────────────────────┐
                          │  Python Flask Backend  │
                          │   (REST API + CORS)    │
                          └─────┬───────┬────┬─────┘
                                │       │    │
       ┌────────────────────────┘       │    └──────────────────────┐
       ▼                                ▼                           ▼
┌──────────────┐             ┌─────────────────────┐      ┌──────────────────┐
│ SQLite Store │             │  Computer Vision    │      │ Optional Live AI │
│ (History &   │             │  (OpenCV + Pillow)  │      │ (Gemini 1.5)     │
│  Meal Plans) │             │  - Keyframe Extract │      │ - Multimodal API │
└──────────────┘             │  - Browning Filter  │      │ - Text Assistant │
                             └─────────────────────┘      └──────────────────┘
```

### Tech Stack Details
- **Frontend**: React 19, Vite, Lucide-React, CSS Custom Properties (Theme Switcher, Print Stylesheets).
- **Backend**: Python 3.10+, Flask 3.1+, Flask-CORS, Werkzeug.
- **Image & Video Processing**: OpenCV (`opencv-python-headless`), Pillow (`PIL`), NumPy.
- **Database**: SQLite 3 (Zero configuration, atomic transactions).
- **Optional AI Integration**: Google Gemini 1.5 Flash Multimodal REST API.

---

## 4. Algorithmic Formulations

### 4.1 Energy Expenditure & Macronutrient Modeling
The meal planner computes Basal Metabolic Rate ($BMR$) via the Mifflin-St Jeor equation:

$$\text{BMR}_{\text{men}} = 10 \cdot W + 6.25 \cdot H - 5 \cdot A + 5$$
$$\text{BMR}_{\text{women}} = 10 \cdot W + 6.25 \cdot H - 5 \cdot A - 161$$

Where:
- $W$ = body weight in kilograms (kg)
- $H$ = body height in centimeters (cm)
- $A$ = age in years

Total Daily Energy Expenditure ($TDEE$) applies an activity coefficient $k \in \{1.2, 1.375, 1.55, 1.725\}$. Goal adjustments enforce safe physiological bounds ($\Delta \le \pm 400 \text{ kcal/day}$) with minimum caloric floors to prevent crash diets.

### 4.2 OpenCV Keyframe Extraction
For video files (`.mp4`, `.webm`), OpenCV samples frames at uniform intervals:
$$\Delta f = \max\left(1, \left\lfloor \frac{N_{\text{total}}}{k + 1} \right\rfloor\right)$$
Keyframes are downsampled to $480\text{px}$ width maintaining aspect ratio and encoded to base64 JPEG buffers for interactive inspection.

---

## 5. Ethical AI, Safety Guardrails & Disclaimers

1. **No False AI Claims**: When no API key is supplied, the UI transparently displays **"Demo Simulation Mode"**. It never claims an external AI neural network analyzed an image if fallback heuristics were used.
2. **Food Safety Limitations**: The system explicitly warns users that visual cues cannot detect odorless bacterial toxins, Salmonella, Listeria, or E. coli.
3. **Non-Regulatory Advisory**: Commercial kitchen hygiene observations are intended for internal staff training and do not constitute an official municipal health department inspection.
4. **Nutritional Approximations**: Nutrition facts are marked as mathematical estimates; users are advised to consult registered dietitians for clinical needs.

---

## 6. Verification & Automated Test Summary

The test suite in `backend/tests/test_api.py` was executed with 8 automated test cases:
- `test_health_check`: Verified system mode, version, and module registry.
- `test_food_analysis_endpoint`: Verified image upload, macro calculations, and disclaimers.
- `test_freshness_analysis_endpoint`: Verified produce categorization and storage tips.
- `test_hygiene_analysis_endpoint`: Verified photo hygiene score and severity ratings.
- `test_video_hygiene_analysis_endpoint`: Verified multi-frame MP4 video upload and OpenCV keyframe extraction.
- `test_cooking_assistant_chat`: Verified pantry ingredient matching and recipe formatting.
- `test_meal_planner_generation`: Verified 7-day schedule output and consolidated grocery list.
- `test_history_flow`: Verified SQLite persistence and audit log retrieval.

**Result: 8/8 tests passed successfully in 0.401s.**

---

## 7. Conclusion

Food Verse AI successfully demonstrates a polished, submission-ready full-stack software application. By integrating computer vision with clean UX and deterministic fallbacks, it provides a stable, resilient platform suitable for academic presentation and real-world demonstration.
