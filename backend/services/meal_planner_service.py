import math

DISCLAIMER = (
    "Nutritional & Dietary Disclaimer: This meal plan is generated for educational and informational purposes "
    "only and does not constitute medical nutrition therapy or personalized clinical advice. Caloric and macro "
    "targets are mathematical approximations based on the Mifflin-St Jeor equation. Consult a registered dietitian "
    "or medical professional prior to initiating substantial dietary changes."
)

SAMPLE_MEAL_POOL = {
    "breakfast": [
        {
            "name": "Steel-Cut Berry Oatmeal with Chia & Walnuts",
            "calories": 380,
            "protein_g": 12,
            "carbs_g": 56,
            "fat_g": 14,
            "diet": ["Vegetarian", "Vegan", "High-Fiber"],
            "ingredients": ["Steel-cut oats", "Almond milk", "Blueberries", "Chia seeds", "Crushed walnuts", "Cinnamon"],
            "prep_time": "12 mins"
        },
        {
            "name": "Spinach, Mushroom & Feta Scrambled Eggs",
            "calories": 350,
            "protein_g": 24,
            "carbs_g": 8,
            "fat_g": 24,
            "diet": ["Vegetarian", "Keto", "Gluten-Free", "High-Protein"],
            "ingredients": ["Eggs", "Baby spinach", "Button mushrooms", "Feta cheese", "Olive oil", "Black pepper"],
            "prep_time": "10 mins"
        },
        {
            "name": "Greek Yogurt Parfait with Granola & Kiwi",
            "calories": 340,
            "protein_g": 22,
            "carbs_g": 42,
            "fat_g": 8,
            "diet": ["Vegetarian", "High-Protein"],
            "ingredients": ["Plain Greek yogurt", "Toasted oat granola", "Sliced kiwi", "Raw honey", "Hemp seeds"],
            "prep_time": "5 mins"
        },
        {
            "name": "Avocado & Mashed Chickpea Tartine",
            "calories": 390,
            "protein_g": 14,
            "carbs_g": 46,
            "fat_g": 18,
            "diet": ["Vegan", "Vegetarian", "High-Fiber"],
            "ingredients": ["Sourdough toast", "Hass avocado", "Cooked chickpeas", "Lemon juice", "Chili flakes"],
            "prep_time": "8 mins"
        }
    ],
    "lunch": [
        {
            "name": "Mediterranean Quinoa, Cucumber & Kalamata Bowl",
            "calories": 480,
            "protein_g": 16,
            "carbs_g": 62,
            "fat_g": 18,
            "diet": ["Vegetarian", "Vegan", "High-Fiber"],
            "ingredients": ["Cooked quinoa", "Persian cucumbers", "Cherry tomatoes", "Kalamata olives", "Chickpeas", "Lemon-tahini dressing"],
            "prep_time": "15 mins"
        },
        {
            "name": "Grilled Lemon Herb Chicken & Roasted Sweet Potato",
            "calories": 520,
            "protein_g": 44,
            "carbs_g": 48,
            "fat_g": 14,
            "diet": ["High-Protein", "Gluten-Free", "Balanced"],
            "ingredients": ["Chicken breast", "Roasted sweet potato cubes", "Steamed green beans", "Olive oil", "Oregano"],
            "prep_time": "25 mins"
        },
        {
            "name": "Tofu Rainbow Noodle Bowl with Peanut Lime Sauce",
            "calories": 460,
            "protein_g": 20,
            "carbs_g": 54,
            "fat_g": 18,
            "diet": ["Vegan", "Vegetarian", "Dairy-Free"],
            "ingredients": ["Crispy baked tofu", "Buckwheat soba noodles", "Shredded purple cabbage", "Carrot ribbons", "Peanut butter lime dressing"],
            "prep_time": "20 mins"
        },
        {
            "name": "Zesty Salmon & Steamed Asparagus Quinoa Plate",
            "calories": 510,
            "protein_g": 38,
            "carbs_g": 36,
            "fat_g": 22,
            "diet": ["Pescatarian", "Gluten-Free", "High-Protein"],
            "ingredients": ["Wild salmon fillet", "Asparagus spears", "Brown rice or quinoa", "Lemon butter glaze", "Dill"],
            "prep_time": "20 mins"
        }
    ],
    "dinner": [
        {
            "name": "Golden Lentil Dal with Turmeric & Basmati Rice",
            "calories": 490,
            "protein_g": 22,
            "carbs_g": 78,
            "fat_g": 9,
            "diet": ["Vegan", "Vegetarian", "High-Fiber"],
            "ingredients": ["Yellow split lentils", "Basmati rice", "Turmeric", "Cumin seeds", "Garlic", "Ginger", "Fresh cilantro"],
            "prep_time": "30 mins"
        },
        {
            "name": "Sheet-Pan Herb Chicken with Broccoli & Baby Potatoes",
            "calories": 510,
            "protein_g": 42,
            "carbs_g": 40,
            "fat_g": 18,
            "diet": ["High-Protein", "Gluten-Free", "Balanced"],
            "ingredients": ["Chicken thighs or breast", "Broccoli florets", "Baby red potatoes", "Rosemary", "Olive oil", "Sea salt"],
            "prep_time": "35 mins"
        },
        {
            "name": "Crispy Tempeh & Bok Choy Stir-Fry with Sesame",
            "calories": 440,
            "protein_g": 26,
            "carbs_g": 38,
            "fat_g": 20,
            "diet": ["Vegan", "Vegetarian", "High-Protein"],
            "ingredients": ["Organic tempeh", "Baby bok choy", "Bell peppers", "Toasted sesame oil", "Tamari soy sauce", "Brown rice"],
            "prep_time": "20 mins"
        },
        {
            "name": "Pan-Seared White Fish with Sautéed Garlic Zucchini",
            "calories": 420,
            "protein_g": 36,
            "carbs_g": 16,
            "fat_g": 22,
            "diet": ["Pescatarian", "Keto", "Low-Carb", "Gluten-Free"],
            "ingredients": ["Cod or tilapia fillet", "Zucchini ribbons", "Cherry tomatoes", "Garlic", "Olive oil", "Lemon"],
            "prep_time": "18 mins"
        }
    ],
    "snack": [
        {
            "name": "Handful of Raw Roasted Almonds & Crisp Apple",
            "calories": 190,
            "protein_g": 5,
            "carbs_g": 22,
            "fat_g": 11,
            "diet": ["Vegan", "Vegetarian", "Gluten-Free"],
            "ingredients": ["Raw almonds", "Honeycrisp apple slices"],
            "prep_time": "2 mins"
        },
        {
            "name": "Carrot & Cucumber Batons with Creamy Hummus",
            "calories": 160,
            "protein_g": 5,
            "carbs_g": 18,
            "fat_g": 8,
            "diet": ["Vegan", "Vegetarian", "Gluten-Free"],
            "ingredients": ["Baby carrots", "English cucumber", "Garlic hummus"],
            "prep_time": "3 mins"
        },
        {
            "name": "Cottage Cheese with Crushed Walnuts & Cinnamon",
            "calories": 180,
            "protein_g": 16,
            "carbs_g": 6,
            "fat_g": 9,
            "diet": ["Vegetarian", "High-Protein", "Low-Carb"],
            "ingredients": ["Low-fat cottage cheese", "Crushed walnuts", "Ground cinnamon"],
            "prep_time": "3 mins"
        }
    ]
}

def calculate_energy_needs(profile: dict) -> dict:
    """
    Calculates Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE)
    using the scientifically established Mifflin-St Jeor formula.
    """
    age = float(profile.get("age", 25))
    weight = float(profile.get("weight_kg", 68))
    height = float(profile.get("height_cm", 170))
    gender = profile.get("gender", "male").lower()
    activity = profile.get("activity_level", "moderately_active").lower()
    goal = profile.get("goal", "maintain").lower()

    # Mifflin-St Jeor formula
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 78

    # Activity multiplier
    multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725
    }
    tdee = bmr * multipliers.get(activity, 1.4)

    # Goal adjustment with safe floors
    if "loss" in goal or "cut" in goal:
        target_calories = max(1350, tdee - 400)
    elif "gain" in goal or "muscle" in goal or "bulk" in goal:
        target_calories = tdee + 350
    else:
        target_calories = tdee

    target_calories = round(target_calories)

    # Dietary macro target splits
    diet_pref = profile.get("dietary_preference", "Balanced").lower()
    if "keto" in diet_pref:
        protein_pct, carbs_pct, fat_pct = 0.25, 0.05, 0.70
    elif "high_protein" in diet_pref or "muscle" in goal:
        protein_pct, carbs_pct, fat_pct = 0.30, 0.45, 0.25
    elif "low_carb" in diet_pref:
        protein_pct, carbs_pct, fat_pct = 0.30, 0.25, 0.45
    else:
        # Balanced standard
        protein_pct, carbs_pct, fat_pct = 0.25, 0.50, 0.25

    protein_g = round((target_calories * protein_pct) / 4)
    carbs_g = round((target_calories * carbs_pct) / 4)
    fat_g = round((target_calories * fat_pct) / 9)

    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "target_calories": target_calories,
        "target_protein_g": protein_g,
        "target_carbs_g": carbs_g,
        "target_fat_g": fat_g,
        "macro_split_percentages": {
            "protein": int(protein_pct * 100),
            "carbs": int(carbs_pct * 100),
            "fat": int(fat_pct * 100)
        }
    }

def generate_weekly_meal_plan(profile: dict) -> dict:
    """
    Generates a personalized 7-day meal plan with daily totals, grocery list, and substitution tips.
    """
    targets = calculate_energy_needs(profile)
    diet_pref = profile.get("dietary_preference", "Balanced").lower()
    allergies = [a.lower() for a in profile.get("allergies", [])]
    disliked = [d.lower() for d in profile.get("disliked_ingredients", [])]
    include_snack = profile.get("meal_frequency", "3_meals_1_snack") != "3_meals"

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = []
    all_ingredients = set()

    for d_idx, day_name in enumerate(days):
        # Pick breakfast, lunch, dinner, snack rotating deterministically
        b_item = SAMPLE_MEAL_POOL["breakfast"][d_idx % len(SAMPLE_MEAL_POOL["breakfast"])]
        l_item = SAMPLE_MEAL_POOL["lunch"][(d_idx + 1) % len(SAMPLE_MEAL_POOL["lunch"])]
        d_item = SAMPLE_MEAL_POOL["dinner"][(d_idx + 2) % len(SAMPLE_MEAL_POOL["dinner"])]
        s_item = SAMPLE_MEAL_POOL["snack"][d_idx % len(SAMPLE_MEAL_POOL["snack"])] if include_snack else None

        day_meals = [
            {"type": "Breakfast", **b_item},
            {"type": "Lunch", **l_item},
            {"type": "Dinner", **d_item}
        ]
        if s_item:
            day_meals.append({"type": "Snack", **s_item})

        day_cals = sum(m["calories"] for m in day_meals)
        day_protein = sum(m["protein_g"] for m in day_meals)
        day_carbs = sum(m["carbs_g"] for m in day_meals)
        day_fat = sum(m["fat_g"] for m in day_meals)

        for m in day_meals:
            for ing in m.get("ingredients", []):
                all_ingredients.add(ing)

        schedule.append({
            "day": day_name,
            "meals": day_meals,
            "daily_totals": {
                "calories": day_cals,
                "protein_g": day_protein,
                "carbs_g": day_carbs,
                "fat_g": day_fat
            }
        })

    # Group ingredients into structured grocery categories
    categorized_grocery = {
        "Fresh Produce": [],
        "Pantry & Grains": [],
        "Proteins & Dairy / Alternatives": [],
        "Herbs, Spices & Oils": []
    }

    for item in sorted(all_ingredients):
        item_lower = item.lower()
        if any(w in item_lower for w in ["spinach", "cucumber", "tomato", "avocado", "broccoli", "carrot", "kiwi", "apple", "asparagus", "bok choy", "mushroom", "lemon", "blueberries"]):
            categorized_grocery["Fresh Produce"].append(item)
        elif any(w in item_lower for w in ["rice", "quinoa", "oat", "sourdough", "granola", "noodle"]):
            categorized_grocery["Pantry & Grains"].append(item)
        elif any(w in item_lower for w in ["chicken", "egg", "tofu", "tempeh", "salmon", "cod", "yogurt", "cottage", "feta", "chickpea", "lentil"]):
            categorized_grocery["Proteins & Dairy / Alternatives"].append(item)
        else:
            categorized_grocery["Herbs, Spices & Oils"].append(item)

    return {
        "targets": targets,
        "schedule": schedule,
        "grocery_list": categorized_grocery,
        "substitutions": [
            {"original": "Chicken breast", "substitute": "Extra firm organic tofu, tempeh, or seitan"},
            {"original": "Greek yogurt", "substitute": "Fortified unsweetened almond or coconut yogurt"},
            {"original": "Salmon fillet", "substitute": "Trout, cod, or marinated king oyster mushroom steaks"},
            {"original": "White rice", "substitute": "Quinoa, riced cauliflower, or farro"}
        ],
        "disclaimer": DISCLAIMER
    }
