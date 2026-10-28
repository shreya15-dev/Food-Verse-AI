import os
import numpy as np
from PIL import Image
from services.ai_service import call_gemini_vision

DEMO_FOOD_CATALOG = [
    {
        "food_name": "Mediterranean Quinoa & Chickpea Bowl",
        "category": "Salads & Bowls",
        "serving_size": "1 bowl (approx 350g)",
        "calories": 420,
        "protein_g": 16.5,
        "carbs_g": 54.0,
        "fat_g": 15.0,
        "fiber_g": 9.2,
        "ingredients": ["Quinoa", "Chickpeas", "Cucumbers", "Cherry Tomatoes", "Kalamata Olives", "Feta Cheese", "Extra Virgin Olive Oil", "Lemon Dressing"],
        "vitamins": ["Vitamin C (45% DV)", "Iron (25% DV)", "Folate (30% DV)", "Magnesium (20% DV)"],
        "health_score": 92,
        "dietary_tags": ["Vegetarian", "High-Fiber", "Mediterranean"],
        "confidence": 0.88,
        "color_family": "green"
    },
    {
        "food_name": "Grilled Herb Chicken Breast with Steamed Veggies",
        "category": "High-Protein Meals",
        "serving_size": "1 plate (approx 320g)",
        "calories": 380,
        "protein_g": 42.0,
        "carbs_g": 14.0,
        "fat_g": 9.5,
        "fiber_g": 5.0,
        "ingredients": ["Boneless Chicken Breast", "Broccoli", "Carrots", "Zucchini", "Garlic Herb Butter", "Black Pepper"],
        "vitamins": ["Vitamin B6 (60% DV)", "Vitamin A (50% DV)", "Niacin (55% DV)", "Potassium (18% DV)"],
        "health_score": 88,
        "dietary_tags": ["High-Protein", "Low-Carb", "Gluten-Free"],
        "confidence": 0.91,
        "color_family": "brown"
    },
    {
        "food_name": "Artisanal Margherita Sourdough Pizza",
        "category": "Italian & Breads",
        "serving_size": "2 slices (approx 220g)",
        "calories": 540,
        "protein_g": 22.0,
        "carbs_g": 68.0,
        "fat_g": 19.5,
        "fiber_g": 3.8,
        "ingredients": ["Fermented Sourdough Crust", "San Marzano Tomato Sauce", "Fresh Mozzarella", "Fresh Basil Leaves", "Cold-Pressed Olive Oil"],
        "vitamins": ["Calcium (35% DV)", "Lycopene (Antioxidant)", "Vitamin B12 (15% DV)"],
        "health_score": 68,
        "dietary_tags": ["Vegetarian"],
        "confidence": 0.86,
        "color_family": "red"
    },
    {
        "food_name": "Avocado & Poached Egg Whole-Wheat Toast",
        "category": "Breakfast & Brunch",
        "serving_size": "2 slices (approx 240g)",
        "calories": 410,
        "protein_g": 18.0,
        "carbs_g": 32.0,
        "fat_g": 24.0,
        "fiber_g": 8.5,
        "ingredients": ["Stone-ground Whole Wheat Bread", "Hass Avocado", "Free-range Eggs", "Chili Flakes", "Microgreens", "Sea Salt"],
        "vitamins": ["Vitamin E (28% DV)", "Vitamin K (35% DV)", "Choline (40% DV)", "Healthy Monounsaturated Fats"],
        "health_score": 89,
        "dietary_tags": ["Vegetarian", "Heart-Healthy", "Whole Grain"],
        "confidence": 0.89,
        "color_family": "green"
    },
    {
        "food_name": "Wild Berry Acai Antioxidant Smoothie Bowl",
        "category": "Smoothies & Bowls",
        "serving_size": "1 bowl (approx 300g)",
        "calories": 330,
        "protein_g": 8.0,
        "carbs_g": 58.0,
        "fat_g": 8.5,
        "fiber_g": 11.0,
        "ingredients": ["Organic Acai Puree", "Blueberries", "Raspberries", "Almond Milk", "Granola", "Chia Seeds", "Coconut Flakes"],
        "vitamins": ["Vitamin C (80% DV)", "Antioxidants (High Anthocyanin)", "Manganese (35% DV)"],
        "health_score": 85,
        "dietary_tags": ["Vegan", "Dairy-Free", "Antioxidant-Rich"],
        "confidence": 0.85,
        "color_family": "purple"
    },
    {
        "food_name": "Paneer Tikka with Mint Chutney & Salad",
        "category": "Indian Cuisine",
        "serving_size": "1 portion (approx 280g)",
        "calories": 440,
        "protein_g": 24.0,
        "carbs_g": 20.0,
        "fat_g": 28.0,
        "fiber_g": 4.5,
        "ingredients": ["Fresh Cottage Cheese (Paneer)", "Bell Peppers", "Onions", "Yogurt Marinade", "Garam Masala", "Mint & Coriander Chutney"],
        "vitamins": ["Calcium (55% DV)", "Phosphorus (30% DV)", "Vitamin A (22% DV)"],
        "health_score": 79,
        "dietary_tags": ["Vegetarian", "High-Protein", "Gluten-Free"],
        "confidence": 0.87,
        "color_family": "orange"
    }
]

def analyze_food_image(image_path: str, filename: str) -> dict:
    """
    Performs food recognition and nutritional analysis.
    Uses Gemini Vision API if key configured; otherwise executes smart heuristic demo fallback.
    """
    disclaimer = (
        "Educational & Informational Disclaimer: Computer vision nutrition estimates are approximations. "
        "Actual caloric and macronutrient values vary significantly based on portion size, cooking oils, "
        "exact ingredients, and preparation techniques. Not medical or dietetic advice."
    )

    # 1. Attempt Live Vision AI if configured
    gemini_prompt = """
    Identify the food items visible in this image. Provide a detailed nutritional analysis.
    Return a strictly formatted JSON object with the following fields:
    - food_name: (string) name of the dish
    - category: (string) e.g., 'Salads', 'High-Protein Meals', 'Desserts', 'Breads & Pastas', etc.
    - serving_size: (string) estimated serving portion
    - calories: (integer) total kcal
    - protein_g: (float) grams of protein
    - carbs_g: (float) grams of carbohydrates
    - fat_g: (float) grams of total fat
    - fiber_g: (float) grams of dietary fiber
    - ingredients: (array of strings) 4-8 identified components/ingredients
    - vitamins: (array of strings) key vitamins/minerals identified
    - health_score: (integer 1-100) estimated overall healthiness score
    - dietary_tags: (array of strings) e.g., 'Vegetarian', 'Vegan', 'Gluten-Free', etc.
    - confidence: (float 0.50 to 0.99) confidence in food recognition
    """

    vision_res = call_gemini_vision(image_path, gemini_prompt) or {}

    if isinstance(vision_res, dict) and vision_res.get("success"):
        data = vision_res["result"]
        data["is_demo"] = False
        data["analysis_mode"] = "Live Multimodal Vision AI (Gemini 1.5 Flash)"
        data["disclaimer"] = disclaimer
        return data

    # 2. Heuristic Demo Fallback
    # Inspect image characteristics with Pillow
    img_width, img_height = 0, 0
    avg_r, avg_g, avg_b = 128, 128, 128
    np_small = np.zeros((50, 50, 3), dtype=np.uint8) 
    try:
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            small = img.resize((50, 50)).convert("RGB")
            np_small = np.array(small)
            avg_r = int(np_small[:, :, 0].mean())
            avg_g = int(np_small[:, :, 1].mean())
            avg_b = int(np_small[:, :, 2].mean())
    except Exception:
        pass

    # Deterministic catalog selection based on image traits or filename hash
    fn_lower = filename.lower()
    selected_item = None
    if any(k in fn_lower for k in ["salad", "green", "veg", "avocado", "bowl"]):
        selected_item = DEMO_FOOD_CATALOG[0]
    elif any(k in fn_lower for k in ["chicken", "meat", "protein", "grilled"]):
        selected_item = DEMO_FOOD_CATALOG[1]
    elif any(k in fn_lower for k in ["pizza", "bread", "cheese", "crust"]):
        selected_item = DEMO_FOOD_CATALOG[2]
    elif any(k in fn_lower for k in ["egg", "toast", "breakfast"]):
        selected_item = DEMO_FOOD_CATALOG[3]
    elif any(k in fn_lower for k in ["berry", "acai", "smoothie", "fruit", "sweet"]):
        selected_item = DEMO_FOOD_CATALOG[4]
    elif any(k in fn_lower for k in ["paneer", "curry", "tikka", "spice"]):
        selected_item = DEMO_FOOD_CATALOG[5]
    else:
        # Demo-only visual heuristic.
        # Detect orange and green pixel regions instead of
        # selecting a dish using only the average image color.

        pixels = np_small.astype(np.int16)
        red = pixels[:, :, 0]
        green = pixels[:, :, 1]
        blue = pixels[:, :, 2]

        orange_mask = (
            (red > 150) &
            (green > 60) &
            (green < 200) &
            (blue < 100) &
            (red > green * 1.15)
        )

        green_mask = (
            (green > 80) &
            (green > red * 1.15) &
            (green > blue * 1.10)
        )

        orange_ratio = float(np.mean(orange_mask))
        green_ratio = float(np.mean(green_mask))

        if orange_ratio > 0.04 and green_ratio > 0.03:
            selected_item = {
                "food_name": "Carrot (Demo Estimate)",
                "category": "Vegetables",
                "serving_size": "Estimated serving (100g)",
                "calories": 41,
                "protein_g": 0.9,
                "carbs_g": 9.6,
                "fat_g": 0.2,
                "fiber_g": 2.8,
                "ingredients": ["Carrot (visual estimate)"],
                "vitamins": ["Vitamin A (estimated)"],
                "health_score": 85,
                "dietary_tags": ["Vegetarian", "Vegan"],
                "confidence": 0.50,
                "color_family": "orange"
            }
        elif green_ratio > 0.10:
            selected_item = DEMO_FOOD_CATALOG[0]
        else:
            selected_item = {
                "food_name": "Food Image — Recognition Unavailable",
                "category": "Unclassified",
                "serving_size": "Unknown",
                "calories": 0,
                "protein_g": 0,
                "carbs_g": 0,
                "fat_g": 0,
                "fiber_g": 0,
                "ingredients": [],
                "vitamins": [],
                "health_score": 0,
                "dietary_tags": [],
                "confidence": 0.0,
                "color_family": "unknown"
            }

    # Build the final result dict from the selected catalog item
    result = dict(selected_item)
    result["is_demo"] = True
    result["analysis_mode"] = "Heuristic Demo Simulation (No Vision API Key Detected)"
    result["disclaimer"] = disclaimer
    return result