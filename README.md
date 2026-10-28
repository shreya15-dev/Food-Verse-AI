# Food Verse AI 🥗

> **Tagline:** *"Smarter Food Choices. Safer Kitchens. Healthier Living."*

Food Verse AI is an end-to-end multimodal food intelligence platform that combines computer vision, image and video processing, conversational culinary reasoning, and clinical macronutrient planning. Designed as an academic capstone and showcase web application, it features a warm, SaaS-inspired design system, a Python Flask REST backend with OpenCV and Pillow, a React 19 + Vite frontend, and an honest, zero-credential heuristic fallback engine that runs 100% offline.

---

## 🌟 Key Modules

### 1. 📊 Executive Dashboard
- **Live KPI Overview**: Real-time counters of total analyses, food identifications, freshness scans, and hygiene audits stored in the local SQLite database.
- **Quick Action Launchpad**: Instant shortcuts to all 5 core modules.
- **Recent Activity Feed**: Chronological list of previous analyses with quick preview and status badges.
- **Transparent AI Badging**: Dynamic indicator showing whether the backend is operating in **Live Multimodal Vision AI Mode** (via Google Gemini) or **Smart Heuristic Demo Simulation Mode**.

### 2. 🍽️ AI Food Recognition & Nutrition
- **Multimodal Uploads**: Supports JPG, JPEG, PNG, and WEBP formats with drag-and-drop, preview, and size validation (up to 15 MB).
- **Nutritional Facts Card**: Computes calories (kcal), macronutrients (protein, carbs, fat, fiber), health score (0–100), and micronutrients/vitamins.
- **Composite Macro Visualizer**: Colored multi-segment energy contribution progress bar and macro percentage cards.
- **Demo Presets**: Pre-configured sample buttons (Quinoa Bowl, Grilled Chicken, Margherita Pizza, Avocado Toast, Berry Smoothie, Paneer Tikka) for instant one-click evaluation without searching for photos.
- **Nutrition Report Printing**: Built-in print action using formatted print stylesheets.
- **Educational Disclaimer**: Cautions that computer vision estimates are approximations and vary by cooking oils, portion volume, and preparation.

### 3. 🍎 Food Freshness Assessment
- **Produce Quality Analysis**: Analyzes fruits, vegetables, and pantry items for visible deterioration, bruising, enzymatic browning, tissue collapse, and fungal mycelium cues.
- **Quality Grading**: Categorizes condition as *"Looks fresh"*, *"Possible deterioration"*, or *"Uncertain / Spoilage detected"*.
- **Visual Evidence Table**: Structured breakdown across surface pigmentation, structural integrity, fungal markers, and moisture.
- **Actionable Guidance**: Practical shelf-life estimates, recommended storage temperatures, and handling suggestions.
- **Food Safety Limitation Notice**: Explicitly emphasizes that cameras cannot detect odorless bacterial toxins, Salmonella, Listeria, or E. coli.

### 4. 🛡️ Restaurant Hygiene Inspector
- **Kitchen Photo & Video Walkthroughs**: Supports still kitchen photos (up to 15 MB) and short video clips (MP4, WEBM, MOV up to 35 MB).
- **OpenCV Keyframe Extraction**: Automatically samples representative frames across video duration using `cv2.VideoCapture`.
- **Sanitation Hazard Detection**: Identifies surface grease, open/uncovered food containers, cross-contamination risks, floor obstructions, and personal protective equipment (PPE) compliance.
- **Observation Cards**: Severity indicators (*High Priority*, *Medium Attention*, *Low / Minor*), specific findings, timestamps for video frames, and corrective action recommendations.
- **Regulatory Notice**: Clarifies that automated audits are advisory and do not replace official municipal health department inspections.

### 5. 🧑‍🍳 Smart Cooking Assistant
- **Conversational Recipe Engine**: Interactive chat interface that transforms available pantry ingredients into delicious recipes.
- **Pantry Tag Manager**: Interactive tags for adding and removing available fridge/pantry ingredients.
- **Culinary Filters**: Filter by cuisine (Mediterranean, Italian, Asian, Indian, American), cooking time (&le;15 min, &le;30 min, &le;45 min), and dietary tags (Vegetarian, Vegan, High-Protein, Gluten-Free, Keto, Dairy-Free).
- **Formatted Recipe Cards**: Step-by-step instructions, preparation times, calorie summaries, and chef's ingredient substitutions.
- **Interactive Tools**: Quick suggestion chips, recipe copy-to-clipboard, conversation reset.

### 6. 📅 Personalized Nutrition & 7-Day Meal Planner
- **Mifflin-St Jeor Energy Modeling**: Calculates Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) based on age, gender, height, weight, and activity level.
- **Safe Goal Adjustments**: Implements conservative calorie adjustments for healthy weight loss (-350 kcal/day) or lean muscle gain (+350 kcal/day) with strict minimum caloric safety bounds.
- **7-Day Day-by-Day Schedule**: Interactive tabbed navigation (Monday through Sunday) featuring breakfast, lunch, dinner, and optional snacks with individual macros and ingredient lists.
- **Consolidated Grocery Checklist**: Unified weekly shopping list grouped by *Fresh Produce*, *Pantry & Grains*, *Proteins & Dairy / Alternatives*, and *Herbs, Spices & Oils* with interactive strike-through checkboxes.
- **Printable Plan**: Formatted export for weekly meal prep.

### 7. 🗄️ Analysis Scan History & Audit Log
- **Persistent SQLite Store**: All image and video scans are automatically saved locally.
- **Module Filter & Search**: Search by dish title, ingredient, or filter by module type.
- **Detail View Modal**: Inspect any previous analysis in a modal.
- **Record Management**: Delete individual records or perform a complete history wipe with confirmation.

---

## 🏗️ System Architecture & Tech Stack

```
smartbridge/
├── backend/
│   ├── app.py                     # Flask REST API endpoints & error handlers
│   ├── config.py                  # Environment config, paths, and upload limits
│   ├── database.py                # SQLite persistence (history, meal plans, preferences)
│   ├── requirements.txt           # Python dependencies (Flask, CORS, Pillow, OpenCV, etc.)
│   ├── services/
│   │   ├── ai_service.py          # Modular Gemini Vision/OpenAI API adapter
│   │   ├── nutrition_service.py   # Nutrition analysis & heuristic catalog fallback
│   │   ├── freshness_service.py   # Produce deterioration & OpenCV browning metrics
│   │   ├── hygiene_service.py     # Video frame extraction & kitchen hazard auditing
│   │   ├── recipe_service.py      # Conversational pantry recipe generator
│   │   └── meal_planner_service.py# Mifflin-St Jeor TDEE & weekly meal scheduler
│   └── tests/
│       └── test_api.py            # Automated unittest test suite (7 tests)
├── frontend/
│   ├── src/
│   │   ├── components/            # Navbar, Sidebar, Footer, ImageUploader, Cards, Modal, Toast
│   │   ├── pages/                 # Dashboard, FoodRecognition, FreshnessCheck, Hygiene, etc.
│   │   ├── services/api.js        # Centralized HTTP client
│   │   ├── App.jsx & main.jsx     # Shell router and toast provider
│   │   └── index.css & App.css    # Responsive SaaS design system & theme variables
│   ├── package.json
│   └── vite.config.js
└── README.md
```

### Technology Highlights
- **Frontend**: React 19, Vite, Lucide React icons, Native CSS custom properties (warm cream `#FAF7F0`, forest green `#1B4332`, terracotta `#E07A5F`), light/dark theme toggle, responsive layout.
- **Backend**: Python 3.10+, Flask 3.1+, Flask-CORS, OpenCV (`opencv-python-headless`), Pillow (`PIL`), SQLite 3.
- **AI Integration**: Modular Google Gemini 1.5 Flash Vision adapter. If no API key is provided, the application runs entirely on smart deterministic heuristics with transparent demo badging.

---

## 🚀 Quickstart Guide

### Prerequisites
1. **Python 3.10+**: Verify with `python --version`
2. **Node.js 18+ & npm**: Verify with `node -v` and `npm -v`

---

### Step 1: Backend Setup & Launch (Terminal 1)

Open Windows PowerShell in the project directory:

```powershell
# Navigate to backend folder
cd c:\Users\shrey\OneDrive\Desktop\smartbridge\backend

# Install Python requirements (if not already installed)
pip install -r requirements.txt

# (Optional) Run the automated unit tests to verify backend integrity
python -m unittest tests/test_api.py

# Launch the Flask API server
python app.py
```

The Flask server will start at:
👉 `http://127.0.0.1:5000` (Health check: `http://127.0.0.1:5000/api/health`)

---

### Step 2: Frontend Setup & Launch (Terminal 2)

Open a **separate** Windows PowerShell window:

```powershell
# Navigate to frontend folder
cd c:\Users\shrey\OneDrive\Desktop\smartbridge\frontend

# Install dependencies (if not already installed)
npm install

# Start the Vite development server
npm run dev
```

The React frontend will start at:
👉 `http://localhost:5173`

Open `http://localhost:5173` in your web browser to use Food Verse AI!

---

## 🔑 Optional: Configuring Live Gemini Vision AI

Food Verse AI is built to work immediately **without any API keys**. However, if you wish to enable live Google Gemini 1.5 Flash multimodal AI:

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. In the `backend/` directory, create or edit `.env`:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
3. Restart the Flask backend server.
4. The system status badge in the top navigation bar will instantly change to **"Live Vision AI Active"**.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check, API mode, and active module list |
| `POST` | `/api/analyze/food` | Upload image (`multipart/form-data: image`); returns nutrition stats |
| `POST` | `/api/analyze/freshness` | Upload image (`multipart/form-data: image`); returns freshness score & cues |
| `POST` | `/api/analyze/hygiene` | Upload image or video (`multipart/form-data: media`); returns hygiene audit |
| `POST` | `/api/recipes/chat` | JSON query with ingredients & filters; returns recipe response |
| `POST` | `/api/meal-plan/generate` | JSON body with user parameters; returns 7-day plan + grocery checklist |
| `GET` | `/api/meal-plan/saved` | Retrieves last saved weekly meal plan and user profile |
| `GET` | `/api/history` | Retrieves stored scans (supports `?limit=50&module_type=food`) |
| `GET` | `/api/history/<id>` | Retrieves full details of a specific scan record |
| `DELETE`| `/api/history/<id>` | Deletes an individual scan record |
| `DELETE`| `/api/history` | Permanently clears all stored scan history |

---

## 🛡️ Disclaimers & Ethical AI Guardrails

1. **Nutritional Approximation**: Nutritional estimations are calculated based on visible surface ingredients and standard portion references. Individual culinary oils, seasoning, and concealed ingredients may alter true values.
2. **Food Safety**: Visual cues cannot establish biological or microbiological safety. Visual inspection does not substitute for laboratory microbial swab tests or temperature probes.
3. **Kitchen Inspections**: Automated kitchen hygiene observations are designed for staff self-auditing and do not represent official certification from municipal health authorities or regulatory agencies.
4. **Clinical Advice**: Meal plans and calorie estimates are for educational guidance and do not replace personalized medical nutrition therapy from a registered dietitian or doctor.

---

## 🎓 Academic Submission Credits

- **Project**: Food Verse AI
- **Course**: Final Year Capstone / Academic Project
- **Architecture**: Full-Stack Multimodal Web Application (React + Vite + Flask + OpenCV + SQLite)
- **Status**: Production & Submission Ready ✅
