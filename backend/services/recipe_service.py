import re
import json
from config import get_ai_api_key
from services.ai_service import call_gemini_text

# ---------------------------------------------------------------------------
# Recipe catalog – expanded with Indian dishes to cover common user requests
# ---------------------------------------------------------------------------
EXPANDED_RECIPE_CATALOG = [
    {
        "id": "shakshuka-1",
        "title": "Classic Mediterranean Shakshuka with Feta",
        "cuisine": "Mediterranean",
        "prep_time_min": 10,
        "cook_time_min": 20,
        "total_time_min": 30,
        "difficulty": "Easy",
        "servings": 3,
        "dietary_tags": ["Vegetarian", "Gluten-Free", "High-Protein"],
        "calories_per_serving": 290,
        "matching_keywords": ["egg", "eggs", "tomato", "tomatoes", "onion", "garlic", "bell pepper", "pepper", "feta", "olive oil", "shakshuka"],
        "description": "Gently poached eggs in a rich, spiced tomato and sweet bell pepper sauce topped with crumbled feta and fresh herbs.",
        "ingredients": [
            {"item": "Free-range eggs", "quantity": "4 large"},
            {"item": "Crushed or diced canned tomatoes", "quantity": "1 can (400g)"},
            {"item": "Red bell pepper, thinly sliced", "quantity": "1 medium"},
            {"item": "Yellow onion, finely diced", "quantity": "1 small"},
            {"item": "Garlic cloves, minced", "quantity": "3 cloves"},
            {"item": "Ground cumin & smoked paprika", "quantity": "1 tsp each"},
            {"item": "Extra virgin olive oil", "quantity": "2 tbsp"},
            {"item": "Crumbled feta cheese", "quantity": "50g"},
            {"item": "Fresh cilantro or parsley", "quantity": "Handful, chopped"}
        ],
        "instructions": [
            "Heat extra virgin olive oil in a wide heavy skillet over medium heat.",
            "Add diced onions and bell peppers; sauté for 5–7 minutes until tender and slightly caramelized.",
            "Stir in minced garlic, ground cumin, smoked paprika, and a pinch of chili flakes; cook for 1 minute until fragrant.",
            "Pour in diced tomatoes, season with salt and black pepper, and simmer gently for 8–10 minutes until sauce thickens.",
            "Create 4 shallow wells in the simmering sauce using a spoon and gently crack an egg into each well.",
            "Cover skillet with a lid and cook on low heat for 5–7 minutes until egg whites are set but yolks remain runny.",
            "Garnish with crumbled feta and chopped fresh cilantro or parsley. Serve warm with crusty bread or pita."
        ],
        "substitutions": [
            "Replace eggs with firm drained tofu blocks for a 100% vegan shakshuka.",
            "Swap canned tomatoes for fresh ripe vine tomatoes cooked down with a splash of water."
        ]
    },
    {
        "id": "tuscan-beans-2",
        "title": "Creamy Tuscan Spinach & Tomato White Bean Stew",
        "cuisine": "Italian",
        "prep_time_min": 8,
        "cook_time_min": 15,
        "total_time_min": 23,
        "difficulty": "Beginner",
        "servings": 4,
        "dietary_tags": ["Vegan", "Vegetarian", "Dairy-Free", "High-Fiber", "Gluten-Free"],
        "calories_per_serving": 310,
        "matching_keywords": ["bean", "beans", "spinach", "tomato", "tomatoes", "garlic", "onion", "olive oil", "broth", "cannellini", "stew", "soup"],
        "description": "Hearty, nourishing white beans simmered with wilted baby spinach, sun-ripened tomatoes, and roasted garlic in an aromatic herb broth.",
        "ingredients": [
            {"item": "Cannellini or white navy beans (cooked/canned)", "quantity": "2 cans (800g), rinsed and drained"},
            {"item": "Fresh baby spinach leaves", "quantity": "4 packed cups"},
            {"item": "Cherry tomatoes, halved", "quantity": "1.5 cups"},
            {"item": "Garlic cloves, minced", "quantity": "4 cloves"},
            {"item": "Vegetable broth", "quantity": "1.5 cups"},
            {"item": "Italian herb seasoning (oregano, thyme, rosemary)", "quantity": "1 tbsp"},
            {"item": "Olive oil", "quantity": "2 tbsp"},
            {"item": "Lemon juice", "quantity": "1 tbsp"}
        ],
        "instructions": [
            "Warm olive oil in a deep pot over medium heat and sauté minced garlic until pale gold (approx 1 min).",
            "Add cherry tomato halves and Italian herbs; cook for 3 minutes until tomatoes start bursting and releasing juices.",
            "Pour in vegetable broth and drained white beans. Bring to a lively simmer.",
            "Mash approximately 1/4 of the beans with a wooden spoon against the pot side to naturally thicken the stew broth.",
            "Stir in baby spinach leaves in batches until completely wilted and bright emerald (about 2 minutes).",
            "Finish with fresh lemon juice, sea salt, and cracked black pepper. Serve with toasted sourdough."
        ],
        "substitutions": [
            "Substitute white beans with chickpeas or cooked green lentils.",
            "Add a splash of unsweetened coconut cream or oat milk for extra silkiness."
        ]
    },
    {
        "id": "garlic-chicken-3",
        "title": "Skillet Garlic Herb Chicken with Crisp Sautéed Veggies",
        "cuisine": "American",
        "prep_time_min": 10,
        "cook_time_min": 15,
        "total_time_min": 25,
        "difficulty": "Easy",
        "servings": 2,
        "dietary_tags": ["High-Protein", "Low-Carb", "Gluten-Free", "Keto"],
        "calories_per_serving": 395,
        "matching_keywords": ["chicken", "breast", "garlic", "butter", "broccoli", "carrot", "zucchini", "herb", "olive oil", "meat", "poultry"],
        "description": "Tender, golden-seared chicken cutlets basted in garlic herb butter alongside crisp-tender garden vegetables.",
        "ingredients": [
            {"item": "Boneless, skinless chicken breasts (halved horizontally)", "quantity": "2 medium breasts (approx 400g)"},
            {"item": "Broccoli florets", "quantity": "2 cups"},
            {"item": "Carrots, sliced into coins", "quantity": "1 large"},
            {"item": "Zucchini, sliced", "quantity": "1 medium"},
            {"item": "Garlic cloves, finely minced", "quantity": "4 cloves"},
            {"item": "Butter or ghee", "quantity": "2 tbsp"},
            {"item": "Olive oil", "quantity": "1 tbsp"},
            {"item": "Dried thyme, rosemary, and smoked paprika", "quantity": "1 tsp each"},
            {"item": "Lemon wedges", "quantity": "For serving"}
        ],
        "instructions": [
            "Pat chicken cutlets dry; season both sides evenly with salt, pepper, thyme, and paprika.",
            "Heat olive oil and 1 tbsp butter in a large skillet over medium-high heat until shimmering.",
            "Place chicken in skillet and sear undisturbed for 4–5 minutes per side until deeply golden and cooked to 165°F (74°C). Transfer to a plate to rest.",
            "In the same skillet, add remaining butter, garlic, broccoli florets, carrots, and zucchini.",
            "Sauté veggies on medium heat for 5 minutes, adding 2 tablespoons of water and covering for 2 minutes to steam-tenderize.",
            "Return chicken and accumulated juices back to skillet, toss with herbs and pan sauce, and serve with fresh lemon wedges."
        ],
        "substitutions": [
            "Replace chicken with firm pressed tofu or salmon fillets.",
            "Swap broccoli and zucchini with bell peppers, green beans, or snap peas."
        ]
    },
    {
        "id": "fried-rice-4",
        "title": "10-Minute Sesame Vegetable & Egg Fried Rice",
        "cuisine": "Asian",
        "prep_time_min": 5,
        "cook_time_min": 10,
        "total_time_min": 15,
        "difficulty": "Beginner",
        "servings": 3,
        "dietary_tags": ["Vegetarian", "Quick & Easy"],
        "calories_per_serving": 340,
        "matching_keywords": ["rice", "egg", "eggs", "soy sauce", "carrot", "peas", "onion", "garlic", "sesame oil", "scallion", "quick"],
        "description": "A rapid weeknight classic utilizing day-old rice, fluffy scrambled eggs, sweet peas, crunchy carrots, and toasted sesame oil.",
        "ingredients": [
            {"item": "Cooked chilled rice (jasmine or basmati)", "quantity": "3 cups"},
            {"item": "Eggs, lightly beaten", "quantity": "3 large"},
            {"item": "Frozen peas and diced carrots", "quantity": "1 cup"},
            {"item": "Scallions/green onions, chopped", "quantity": "3 stalks"},
            {"item": "Garlic cloves, minced", "quantity": "2 cloves"},
            {"item": "Low-sodium soy sauce or tamari", "quantity": "2.5 tbsp"},
            {"item": "Toasted sesame oil", "quantity": "1.5 tbsp"},
            {"item": "High-heat cooking oil", "quantity": "1 tbsp"}
        ],
        "instructions": [
            "Heat cooking oil in a wok or deep skillet over high heat. Pour in beaten eggs and scramble softly for 60 seconds; transfer eggs to a small bowl.",
            "Add another teaspoon of oil, then add minced garlic, white parts of scallions, peas, and carrots. Stir-fry vigorously for 2 minutes.",
            "Add chilled rice, breaking apart clumps with your spatula.",
            "Drizzle soy sauce and toasted sesame oil evenly across the rice. Toss continuously for 3–4 minutes until grains are toasted and aromatic.",
            "Fold the scrambled eggs and sliced green scallion tops back in. Toss for 30 seconds and serve immediately."
        ],
        "substitutions": [
            "Use quinoa or cauliflower rice for a low-carb alternative.",
            "Replace eggs with crumbled seasoned tofu for vegan fried rice."
        ]
    },
    {
        "id": "tofu-stirfry-5",
        "title": "Crispy Golden Tofu & Broccoli in Ginger Soy Glaze",
        "cuisine": "Asian",
        "prep_time_min": 12,
        "cook_time_min": 12,
        "total_time_min": 24,
        "difficulty": "Easy",
        "servings": 3,
        "dietary_tags": ["Vegan", "Vegetarian", "Dairy-Free", "High-Protein"],
        "calories_per_serving": 320,
        "matching_keywords": ["tofu", "broccoli", "ginger", "soy sauce", "garlic", "sesame", "cornstarch", "rice", "vegan"],
        "description": "Crispy pan-fried tofu cubes and tender broccoli tossed in an umami-rich garlic ginger reduction.",
        "ingredients": [
            {"item": "Extra firm tofu, pressed and cubed", "quantity": "1 block (400g)"},
            {"item": "Cornstarch", "quantity": "2 tbsp (for coating)"},
            {"item": "Broccoli florets", "quantity": "3 cups"},
            {"item": "Fresh ginger, grated", "quantity": "1 tbsp"},
            {"item": "Garlic cloves, minced", "quantity": "3 cloves"},
            {"item": "Soy sauce or tamari", "quantity": "3 tbsp"},
            {"item": "Maple syrup or honey", "quantity": "1 tbsp"},
            {"item": "Sesame seeds", "quantity": "1 tbsp"}
        ],
        "instructions": [
            "Toss pressed tofu cubes with cornstarch and a pinch of salt until lightly coated.",
            "Pan-fry in 2 tbsp oil on medium-high heat for 8 minutes, turning occasionally until all sides are crisp and golden. Remove to plate.",
            "Stir-fry broccoli with 2 tbsp water for 3 minutes until vibrant green.",
            "Whisk soy sauce, grated ginger, minced garlic, maple syrup, and 2 tbsp water. Pour into skillet.",
            "Simmer sauce for 1 minute until it bubbles and thickens. Toss crispy tofu back in to coat evenly.",
            "Sprinkle toasted sesame seeds and serve warm over steamed jasmine rice."
        ],
        "substitutions": [
            "Use tempeh, seitan, or edamame instead of tofu.",
            "Swap broccoli for snap peas, asparagus, or bell peppers."
        ]
    },
    {
        "id": "creamy-pasta-6",
        "title": "Avocado & Spinach Creamy Garlic Penne",
        "cuisine": "Italian",
        "prep_time_min": 10,
        "cook_time_min": 12,
        "total_time_min": 22,
        "difficulty": "Beginner",
        "servings": 3,
        "dietary_tags": ["Vegetarian", "Vegan", "Dairy-Free"],
        "calories_per_serving": 410,
        "matching_keywords": ["pasta", "penne", "avocado", "spinach", "garlic", "lemon", "basil", "noodle"],
        "description": "Silky, nutrient-packed plant-based pasta sauce made with blended ripe avocados, baby spinach, fresh basil, garlic, and lemon zest.",
        "ingredients": [
            {"item": "Penne or rigatoni pasta", "quantity": "250g"},
            {"item": "Ripe Hass avocados", "quantity": "2 medium"},
            {"item": "Fresh baby spinach", "quantity": "2 packed cups"},
            {"item": "Garlic cloves", "quantity": "2 cloves"},
            {"item": "Fresh lemon juice & zest", "quantity": "1 lemon"},
            {"item": "Extra virgin olive oil", "quantity": "2 tbsp"},
            {"item": "Nutritional yeast or parmesan", "quantity": "3 tbsp"}
        ],
        "instructions": [
            "Boil pasta in well-salted water until al dente according to package instructions. Reserve 1/2 cup pasta cooking water, then drain.",
            "In a food processor or blender, combine avocado flesh, baby spinach, garlic, lemon juice, olive oil, salt, and black pepper.",
            "Blend until velvety smooth, streaming in 2-4 tbsp reserved warm pasta water until desired creamy consistency is achieved.",
            "Toss hot drained pasta immediately with the creamy avocado sauce.",
            "Garnish with lemon zest, cracked pepper, and nutritional yeast or shaved parmesan. Serve immediately."
        ],
        "substitutions": [
            "Use gluten-free chickpea or lentil pasta for extra protein and fiber.",
            "Add halved cherry tomatoes or toasted pine nuts for crunch."
        ]
    },
    {
        "id": "dal-tadka-7",
        "title": "Homestyle Yellow Lentil Dal Tadka with Cumin & Garlic",
        "cuisine": "Indian",
        "prep_time_min": 10,
        "cook_time_min": 25,
        "total_time_min": 35,
        "difficulty": "Easy",
        "servings": 4,
        "dietary_tags": ["Vegan", "Vegetarian", "Gluten-Free", "High-Fiber", "High-Protein"],
        "calories_per_serving": 280,
        "matching_keywords": ["lentil", "lentils", "dal", "turmeric", "cumin", "garlic", "ginger", "tomato", "chili", "indian", "curry"],
        "description": "Comforting, golden split lentils cooked to creamy perfection and infused with a fragrant tempered ghee/oil tadka of cumin seeds, garlic, and dried red chilies.",
        "ingredients": [
            {"item": "Toor dal or yellow split moong dal", "quantity": "1 cup (rinsed)"},
            {"item": "Turmeric powder", "quantity": "1/2 tsp"},
            {"item": "Tomatoes, chopped", "quantity": "2 medium"},
            {"item": "Garlic cloves, thinly sliced", "quantity": "4 cloves"},
            {"item": "Cumin seeds", "quantity": "1 tsp"},
            {"item": "Ghee or coconut oil", "quantity": "2 tbsp"},
            {"item": "Fresh cilantro leaves", "quantity": "1/4 cup"}
        ],
        "instructions": [
            "Simmer rinsed lentils in 3 cups water with turmeric and 1 tsp salt for 20 minutes until soft and creamy.",
            "In a separate small pan, heat ghee or oil over medium heat. Add cumin seeds and let them sizzle for 30 seconds.",
            "Add sliced garlic, grated ginger, and chopped green chili; sauté until garlic turns light golden.",
            "Add chopped tomatoes and cook for 3 minutes until softened.",
            "Pour the sizzling aromatic tadka into the cooked dal. Stir well and simmer for 2 minutes to meld flavors.",
            "Stir in fresh cilantro and a squeeze of fresh lemon juice. Serve hot with steamed basmati rice or flatbread."
        ],
        "substitutions": [
            "Use red lentils (masoor dal) which cook in just 15 minutes.",
            "Use coconut oil instead of ghee for a 100% vegan preparation."
        ]
    },
    # ── NEW: Indian dishes added to fix irrelevant responses ────────────────
    {
        "id": "veg-pulao-8",
        "title": "Fragrant Vegetable Pulao (Serves 2)",
        "cuisine": "Indian",
        "prep_time_min": 10,
        "cook_time_min": 20,
        "total_time_min": 30,
        "difficulty": "Easy",
        "servings": 2,
        "dietary_tags": ["Vegetarian", "Vegan", "Gluten-Free"],
        "calories_per_serving": 380,
        "matching_keywords": [
            "pulao", "pulav", "rice", "basmati", "vegetable", "vegetables", "mixed veg",
            "carrot", "peas", "beans", "potato", "onion", "cumin", "bay leaf", "clove",
            "cinnamon", "cardamom", "indian", "spice", "ghee", "mint"
        ],
        "description": "Aromatic basmati rice cooked with whole spices and colourful mixed vegetables — a quick, one-pot Indian classic.",
        "ingredients": [
            {"item": "Basmati rice, washed and soaked 20 min", "quantity": "1 cup"},
            {"item": "Water or vegetable stock", "quantity": "1.75 cups"},
            {"item": "Ghee or oil", "quantity": "2 tbsp"},
            {"item": "Onion, thinly sliced", "quantity": "1 medium"},
            {"item": "Green peas (fresh or frozen)", "quantity": "1/3 cup"},
            {"item": "Carrot, diced small", "quantity": "1 small"},
            {"item": "French beans, chopped", "quantity": "1/4 cup"},
            {"item": "Potato, diced (optional)", "quantity": "1 small"},
            {"item": "Whole spices: bay leaf, cloves, cinnamon, cardamom", "quantity": "1 bay leaf, 3 cloves, 1-inch cinnamon, 2 cardamom"},
            {"item": "Cumin seeds", "quantity": "1 tsp"},
            {"item": "Ginger-garlic paste", "quantity": "1 tsp"},
            {"item": "Salt", "quantity": "To taste"},
            {"item": "Fresh mint or coriander leaves", "quantity": "Handful"}
        ],
        "instructions": [
            "Soak basmati rice for 20 minutes, then drain and set aside.",
            "Heat ghee in a heavy-bottomed pot over medium heat. Add cumin seeds and whole spices; sizzle for 30 seconds.",
            "Add sliced onion and fry until golden brown, about 5–6 minutes.",
            "Stir in ginger-garlic paste and cook for 1 minute.",
            "Add all the vegetables (carrot, beans, peas, potato). Mix well and cook for 2 minutes.",
            "Drain the soaked rice and add it to the pot. Gently stir to coat with ghee and spices.",
            "Pour in 1.75 cups of water or stock. Add salt. Bring to a boil, then reduce heat to the lowest setting.",
            "Cover tightly and cook on very low heat for 15 minutes. Do not lift the lid during cooking.",
            "Remove from heat and let it rest, covered, for 5 minutes. Fluff gently with a fork.",
            "Garnish with fresh mint or coriander and serve with raita or pickle."
        ],
        "substitutions": [
            "Replace ghee with neutral oil for a vegan version.",
            "Use cauliflower florets, corn, or mushrooms instead of potatoes.",
            "Swap basmati for long-grain parboiled rice — increase water to 2 cups."
        ]
    },
    {
        "id": "paneer-curry-9",
        "title": "Creamy Paneer Tikka Masala",
        "cuisine": "Indian",
        "prep_time_min": 15,
        "cook_time_min": 20,
        "total_time_min": 35,
        "difficulty": "Easy",
        "servings": 3,
        "dietary_tags": ["Vegetarian", "Gluten-Free", "High-Protein"],
        "calories_per_serving": 420,
        "matching_keywords": [
            "paneer", "paneer curry", "tikka masala", "tikka", "masala", "cottage cheese",
            "cream", "tomato", "onion", "cashew", "curry", "indian", "spice",
            "garam masala", "turmeric", "cumin", "coriander"
        ],
        "description": "Succulent cubes of paneer simmered in a rich, smoky tomato and cream gravy spiced with garam masala.",
        "ingredients": [
            {"item": "Paneer, cubed", "quantity": "250g"},
            {"item": "Tomatoes, pureed", "quantity": "3 medium (or 1 cup canned)"},
            {"item": "Onion, finely chopped", "quantity": "1 large"},
            {"item": "Fresh cream or cashew paste", "quantity": "3 tbsp"},
            {"item": "Ginger-garlic paste", "quantity": "1.5 tsp"},
            {"item": "Kashmiri red chili powder", "quantity": "1 tsp"},
            {"item": "Garam masala", "quantity": "1 tsp"},
            {"item": "Cumin seeds", "quantity": "1/2 tsp"},
            {"item": "Butter or oil", "quantity": "2 tbsp"},
            {"item": "Salt", "quantity": "To taste"},
            {"item": "Fresh coriander", "quantity": "For garnish"}
        ],
        "instructions": [
            "Heat butter in a pan; add cumin seeds and let them splutter.",
            "Add finely chopped onion and sauté until golden (about 7 min).",
            "Stir in ginger-garlic paste and cook for 1 minute.",
            "Add tomato puree, chili powder, and a pinch of salt. Cook on medium heat for 6–8 minutes until oil separates from the masala.",
            "Stir in garam masala and fresh cream (or cashew paste). Mix well.",
            "Add paneer cubes and gently fold them in. Simmer on low heat for 5 minutes.",
            "Taste and adjust salt. Garnish with fresh coriander and serve with naan or jeera rice."
        ],
        "substitutions": [
            "No tomatoes? Use 2 tbsp yogurt + 1 tbsp tomato ketchup as a quick substitute for the tangy base.",
            "Replace cream with coconut milk for a dairy-reduced, slightly sweet variation.",
            "Use firm tofu instead of paneer for a vegan version."
        ]
    },
    {
        "id": "upma-10",
        "title": "Quick Vegetable Upma — Savory Semolina Breakfast",
        "cuisine": "Indian",
        "prep_time_min": 5,
        "cook_time_min": 10,
        "total_time_min": 15,
        "difficulty": "Beginner",
        "servings": 2,
        "dietary_tags": ["Vegetarian", "Quick & Easy"],
        "calories_per_serving": 280,
        "matching_keywords": [
            "upma", "semolina", "rava", "sooji", "suji", "breakfast", "morning",
            "quick", "vegetarian", "onion", "mustard", "curry leaf", "peas",
            "carrot", "vegetable", "indian", "15 min", "15 minutes"
        ],
        "description": "A South Indian breakfast staple — fluffy roasted semolina cooked with tempered spices and crunchy vegetables. Ready in 15 minutes.",
        "ingredients": [
            {"item": "Fine semolina (rava / sooji), dry-roasted", "quantity": "1 cup"},
            {"item": "Hot water", "quantity": "2.5 cups"},
            {"item": "Oil", "quantity": "2 tbsp"},
            {"item": "Mustard seeds", "quantity": "1/2 tsp"},
            {"item": "Dry red chili", "quantity": "1"},
            {"item": "Curry leaves", "quantity": "8–10"},
            {"item": "Green chili, slit", "quantity": "1"},
            {"item": "Onion, finely chopped", "quantity": "1 medium"},
            {"item": "Mixed vegetables (carrot, peas, beans)", "quantity": "1/2 cup"},
            {"item": "Salt", "quantity": "To taste"},
            {"item": "Fresh coriander and lemon juice", "quantity": "For garnish"}
        ],
        "instructions": [
            "Dry-roast semolina in the pan over medium heat for 3–4 minutes until light golden and fragrant. Set aside.",
            "In the same pan, heat oil. Add mustard seeds; when they splutter add dry red chili and curry leaves.",
            "Add green chili and chopped onion; sauté for 2 minutes until onion turns translucent.",
            "Add mixed vegetables and cook for 2 minutes.",
            "Pour in 2.5 cups of hot water carefully; add salt. Bring to a boil.",
            "Reduce heat to medium-low and gradually pour in roasted semolina while stirring constantly to avoid lumps.",
            "Mix well, cover, and cook for 2 minutes. Fluff with a fork.",
            "Squeeze lemon juice, garnish with coriander, and serve hot with coconut chutney."
        ],
        "substitutions": [
            "No semolina? Use fine oats (dalia) instead for a healthier variation.",
            "Add roasted cashews or peanuts for extra crunch and protein."
        ]
    },
    {
        "id": "poha-11",
        "title": "Flattened Rice Poha with Peas & Peanuts",
        "cuisine": "Indian",
        "prep_time_min": 5,
        "cook_time_min": 10,
        "total_time_min": 15,
        "difficulty": "Beginner",
        "servings": 2,
        "dietary_tags": ["Vegetarian", "Vegan", "Gluten-Free", "Quick & Easy"],
        "calories_per_serving": 260,
        "matching_keywords": [
            "poha", "flattened rice", "breakfast", "morning", "quick", "15 min",
            "vegetarian", "peas", "onion", "mustard", "turmeric", "peanut", "indian"
        ],
        "description": "Light and tangy flattened rice sautéed with onions, green peas, peanuts, and a squeeze of lemon — a beloved Indian breakfast.",
        "ingredients": [
            {"item": "Thick flattened rice (poha), rinsed and drained", "quantity": "1.5 cups"},
            {"item": "Oil", "quantity": "1.5 tbsp"},
            {"item": "Mustard seeds", "quantity": "1/2 tsp"},
            {"item": "Onion, finely chopped", "quantity": "1 medium"},
            {"item": "Green chili, slit", "quantity": "1"},
            {"item": "Turmeric powder", "quantity": "1/4 tsp"},
            {"item": "Green peas", "quantity": "1/4 cup"},
            {"item": "Roasted peanuts", "quantity": "2 tbsp"},
            {"item": "Salt and sugar", "quantity": "To taste"},
            {"item": "Lemon juice", "quantity": "1 tsp"},
            {"item": "Fresh coriander", "quantity": "For garnish"}
        ],
        "instructions": [
            "Gently rinse poha under cold water in a colander until soft. Drain and set aside (do not soak).",
            "Heat oil in a pan; add mustard seeds and wait for them to pop.",
            "Add green chili, peanuts, and onion. Sauté for 2 minutes.",
            "Add peas and cook for 1 minute.",
            "Add turmeric, salt, and a pinch of sugar. Mix.",
            "Add the softened poha and fold gently without breaking the flakes.",
            "Cover and cook on low heat for 2 minutes.",
            "Squeeze lemon juice, garnish with coriander, and serve immediately."
        ],
        "substitutions": [
            "Replace peas with corn kernels or finely diced carrot.",
            "Add a few curry leaves and a pinch of hing (asafoetida) with the mustard for extra aroma."
        ]
    },
    {
        "id": "aloo-paratha-12",
        "title": "Stuffed Aloo Paratha — Spiced Potato Flatbread",
        "cuisine": "Indian",
        "prep_time_min": 20,
        "cook_time_min": 15,
        "total_time_min": 35,
        "difficulty": "Easy",
        "servings": 2,
        "dietary_tags": ["Vegetarian", "High-Fiber"],
        "calories_per_serving": 350,
        "matching_keywords": [
            "paratha", "aloo paratha", "chapati", "roti", "flatbread", "potato",
            "wheat flour", "dough", "breakfast", "indian", "stuffed", "spice",
            "cumin", "coriander powder", "chili"
        ],
        "description": "Crispy on the outside, pillowy soft inside — whole-wheat flatbreads filled with a spiced mashed potato mixture, pan-fried with butter or ghee.",
        "ingredients": [
            {"item": "Whole-wheat flour (atta)", "quantity": "1.5 cups"},
            {"item": "Water (lukewarm)", "quantity": "Approx 1/2 cup"},
            {"item": "Salt", "quantity": "1/2 tsp"},
            {"item": "Boiled and mashed potatoes", "quantity": "2 medium"},
            {"item": "Cumin seeds", "quantity": "1/2 tsp"},
            {"item": "Coriander powder", "quantity": "1/2 tsp"},
            {"item": "Green chili, finely chopped", "quantity": "1"},
            {"item": "Fresh coriander leaves, chopped", "quantity": "2 tbsp"},
            {"item": "Ghee or butter", "quantity": "2 tbsp (for cooking)"}
        ],
        "instructions": [
            "Knead flour, salt, and water into a soft, smooth dough. Rest for 10 minutes under a damp cloth.",
            "Mix mashed potatoes with cumin, coriander powder, green chili, salt, and fresh coriander leaves.",
            "Divide dough into balls (golf-ball size). Roll each into a 4-inch disc.",
            "Place 1–2 tbsp potato filling in the centre. Gather the edges and pinch to seal. Flatten gently.",
            "Roll out into a 7–8 inch circle — go slowly to keep filling intact.",
            "Heat a tawa or heavy skillet over medium-high heat. Cook paratha for 1–2 minutes per side until brown spots appear.",
            "Apply a small knob of ghee or butter on each side and cook for another 30 seconds each side until crisp.",
            "Serve hot with plain yogurt, pickle, or butter."
        ],
        "substitutions": [
            "Replace potato filling with crumbled paneer + spices for a protein-rich variation.",
            "Use cauliflower (gobi) instead of potato for a lower-carb option."
        ]
    }
]

# ---------------------------------------------------------------------------
# Culinary advice catalog – technique tips and common substitutions
# ---------------------------------------------------------------------------
CULINARY_ADVICE_CATALOG = {
    "soft_chapati": (
        "### How to Make Soft Chapatis / Rotis That Stay Soft\n\n"
        "Hard chapatis are one of the most common kitchen frustrations. Here are the key fixes:\n\n"
        "**1. Dough Hydration**\n"
        "- Use **warm water** (not cold) while kneading — warm water activates gluten more evenly.\n"
        "- The dough should feel as soft as an earlobe. If it springs back firmly, add 1 tbsp warm water at a time and knead again.\n\n"
        "**2. Resting the Dough**\n"
        "- Rest the kneaded dough for **at least 20–30 minutes** covered with a damp cloth or an inverted bowl. This relaxes the gluten and makes rolling easier and the chapati softer.\n\n"
        "**3. Rolling Technique**\n"
        "- Roll with **light, even pressure**. Over-rolling toughens the dough.\n"
        "- Aim for uniform thickness — thin edges burn while the centre stays raw.\n\n"
        "**4. Cooking Temperature**\n"
        "- Cook on a **preheated tawa on high-medium heat**. A cold or too-low tawa causes chapatis to dry out instead of puffing.\n"
        "- Cook the first side for 30–40 seconds (you should see small bubbles form), flip, cook the second side for 30 seconds, then press the edges with a cloth to puff it up.\n\n"
        "**5. Keeping Them Soft**\n"
        "- Stack hot chapatis in a cloth-lined container (like a casserole dish) immediately after cooking. The steam trapped inside keeps them soft.\n"
        "- Apply a thin coat of **ghee or butter** as soon as each chapati comes off the tawa.\n\n"
        "**Common mistakes to avoid:**\n"
        "- Using stale flour or cold water\n"
        "- Skipping the rest time\n"
        "- Cooking on low heat for too long\n"
        "- Leaving cooked chapatis open and exposed to air"
    ),

    "tomato_substitute_curry": (
        "### Tomato Substitutes for Indian Curry\n\n"
        "Tomatoes provide **acidity, body, and colour** in most Indian gravies. Here are practical alternatives:\n\n"
        "| Substitute | Amount (per 2 medium tomatoes) | Notes |\n"
        "|---|---|---|\n"
        "| **Plain yogurt (dahi)** | 1/2 cup | Adds tang and creaminess — ideal for paneer/chicken curries |\n"
        "| **Tamarind paste** | 1 tbsp | Stronger tartness; use sparingly. Best in dal, sambar, rasam |\n"
        "| **Amchur (dry mango powder)** | 1 tsp | Adds sourness without moisture — great for dry sabzis |\n"
        "| **Kokum** | 2–3 petals (soaked) | Used in coastal curries (Goan, Konkan style) |\n"
        "| **Tomato ketchup** | 2 tbsp | Convenient pantry swap; slightly sweet |\n"
        "| **Lemon juice** | 1.5 tbsp | Adds clean acidity; add at the end of cooking |\n"
        "| **Canned tomato paste** | 1 tbsp + 3 tbsp water | Concentrated; dilute before using |\n\n"
        "**For paneer curry specifically:**\n"
        "Mix **3 tbsp plain yogurt + 1 tbsp cashew paste + a pinch of sugar** — this gives a rich, tangy, creamy base without any tomato."
    ),

    "egg_substitution": (
        "### Smart Culinary Substitutions for Eggs\n\n"
        "- **In Baking (Cakes/Muffins)**: Use **1/4 cup unsweetened applesauce** or **1/2 mashed ripe banana** per egg.\n"
        "- **Binding (Burgers/Patties)**: Use **1 tbsp ground chia or flaxseed mixed with 3 tbsp warm water** (let sit for 5 min until gel-like).\n"
        "- **Savory Scrambles**: Use **crumbled firm tofu** sautéed with nutritional yeast, pinch of turmeric (for golden color), and black salt (kala namak).\n"
        "- **In Pancakes/Waffles**: Use **1/4 cup plain yogurt** or silken tofu blended smooth."
    ),

    "buttermilk_substitution": (
        "### How to Make Homemade Buttermilk in 5 Minutes\n\n"
        "- Combine **1 cup whole milk or unsweetened soy milk** with **1 tablespoon lemon juice or white vinegar**.\n"
        "- Stir and let stand undisturbed at room temperature for 5 to 10 minutes until slightly curdled and thickened.\n"
        "- Use 1:1 in pancakes, biscuits, marinades, or dressings."
    ),

    "fluffy_eggs": (
        "### Chef's Secret for Fluffy, Velvety Scrambled Eggs\n\n"
        "1. **Low & Slow Heat**: Cook over medium-low heat. High heat drives out moisture, resulting in rubbery eggs.\n"
        "2. **Continuous Sweeping**: Use a silicone spatula to push large, soft curds from edges to center.\n"
        "3. **Take Off Heat Early**: Remove from stove while eggs are still glossy and slightly wet; residual pan heat finishes cooking them to perfection."
    ),

    "rice_mushy": (
        "### How to Cook Perfect Non-Sticky Rice\n\n"
        "**For stovetop basmati / long-grain rice:**\n"
        "1. **Rinse** rice 2–3 times until water runs clear (removes excess starch).\n"
        "2. **Soak** for 20–30 minutes; drain.\n"
        "3. Use a **1:1.5 ratio** (1 cup rice : 1.5 cups water for basmati; 1:2 for regular white rice).\n"
        "4. Bring to a boil, then reduce to the **lowest heat possible**, cover, and cook for 12–15 min.\n"
        "5. **Do not stir** during cooking — stirring breaks starch granules and causes mushiness.\n"
        "6. After cooking, rest off heat for 5 minutes with the lid on, then fluff with a fork."
    ),

    "food_storage": (
        "### Common Food Storage Tips\n\n"
        "- **Leafy greens**: Wrap in a dry paper towel and store in an airtight container in the fridge (up to 5 days).\n"
        "- **Onions & garlic**: Store in a cool, dark, ventilated spot — NOT in the fridge (moisture makes them rot faster).\n"
        "- **Cooked rice**: Refrigerate within 1 hour of cooking; consume within 2 days. Never leave cooked rice at room temperature for more than 2 hours.\n"
        "- **Paneer**: Submerge in cold water, change water daily; keeps 3–4 days in the fridge. Freeze for up to 1 month.\n"
        "- **Tomatoes**: Store at room temperature; refrigeration destroys flavour. Use ripe tomatoes within 3–5 days.\n"
        "- **Bread**: Room temperature in an airtight bag (up to 3 days) or freeze slices (up to 3 months)."
    ),
}

# ---------------------------------------------------------------------------
# Intent detection helpers
# ---------------------------------------------------------------------------

def _extract_conversation_context(conversation_history: list) -> dict:
    """
    Extracts key context from previous messages (e.g. last dish discussed).
    """
    context = {"last_dish": None, "last_title": None}
    if not conversation_history:
        return context

    # Check from newest to oldest
    for m in reversed(conversation_history):
        if not isinstance(m, dict):
            continue
        text = str(m.get("text", "")).lower()
        if not text:
            continue
        for dish, title in [
            ("pulao", "Vegetable Pulao"),
            ("pulav", "Vegetable Pulao"),
            ("chapati", "Chapatis / Rotis"),
            ("roti", "Chapatis / Rotis"),
            ("paneer", "Paneer Curry"),
            ("upma", "Vegetable Upma"),
            ("poha", "Poha"),
            ("paratha", "Aloo Paratha"),
            ("shakshuka", "Shakshuka"),
            ("dal", "Dal Tadka"),
            ("pasta", "Penne Pasta"),
            ("fried rice", "Fried Rice"),
            ("chicken", "Garlic Chicken"),
            ("tofu", "Crispy Tofu Stir-fry"),
            ("stew", "White Bean Stew"),
        ]:
            if dish in text:
                context["last_dish"] = dish
                context["last_title"] = title
                break
        if context["last_dish"]:
            break

    return context


def _handle_followup_query(prompt_lower: str, context: dict) -> str | None:
    """
    Handles follow-up queries that refer to the previous dish/topic in conversation.
    """
    last_dish = context.get("last_dish")
    last_title = context.get("last_title", "this dish")

    # Pressure cooker conversion
    if any(k in prompt_lower for k in ["pressure cooker", "cooker", "whistle", "whistles"]):
        if last_dish in ("pulao", "pulav", "rice"):
            return (
                "### Making Vegetable Pulao in a Pressure Cooker\n\n"
                "Yes, absolutely! Making vegetable pulao in a pressure cooker is even faster and gives wonderfully fluffy rice if you follow these steps:\n\n"
                "**Key Adjustments:**\n"
                "- **Water ratio:** Reduce water slightly to **1.5 cups** per 1 cup of soaked basmati rice (compared to 1.75 cups in an open pot), because no steam escapes under pressure.\n"
                "- **Whistles:** Cook on medium-high heat for **1 to 2 whistles** (or 1 whistle on high heat, then immediately lower to low heat for 2 minutes and turn off).\n"
                "- **Pressure release:** Let the pressure release **naturally** (10–12 minutes). Do not force-open the valve, as the residual steam finishes cooking the rice grains evenly.\n\n"
                "**Step-by-Step in Cooker:**\n"
                "1. Heat 2 tbsp ghee directly in the pressure cooker. Sauté cumin seeds, bay leaf, cinnamon, cloves, and cardamom for 30 seconds.\n"
                "2. Add sliced onions and fry until golden (5–6 mins).\n"
                "3. Add ginger-garlic paste and chopped vegetables (peas, carrots, beans); sauté for 2 minutes.\n"
                "4. Add drained, soaked basmati rice and gently stir for 1 minute to coat with ghee.\n"
                "5. Pour in 1.5 cups water and salt to taste. Stir once.\n"
                "6. Close the lid and cook for **1 to 2 whistles** on medium flame.\n"
                "7. Turn off heat and wait for pressure to release completely. Open and gently fluff with a fork.\n\n"
                "Serve hot with cucumber raita or pickle!"
            )
        elif last_dish == "dal":
            return (
                "### Cooking Dal in a Pressure Cooker\n\n"
                "Yes! For yellow split lentils (toor or moong dal):\n"
                "- Use **3 cups water per 1 cup dal**.\n"
                "- Add 1/2 tsp turmeric, 1 tsp salt, and 1/2 tsp oil (prevents frothing).\n"
                "- Cook for **3 to 4 whistles** on medium heat.\n"
                "- Allow pressure to release naturally, then whisk smooth and add your aromatic tadka."
            )
        else:
            return (
                f"### Pressure Cooker Adaptation for {last_title}\n\n"
                "To adapt this dish to a pressure cooker:\n"
                "- **Reduce liquid by 15–20%**, as steam cannot escape during pressure cooking.\n"
                "- For rice and vegetables: cook for **1–2 whistles** on medium flame.\n"
                "- For lentils and beans: cook for **3–4 whistles**.\n"
                "- Always allow pressure to release naturally before opening to ensure even cooking."
            )

    # Side dishes / accompaniments
    if any(k in prompt_lower for k in ["serve with", "side dish", "sides", "accompaniment", "pair with", "eat with"]):
        if last_dish in ("pulao", "pulav", "biryani"):
            return (
                "### Best Accompaniments for Vegetable Pulao\n\n"
                "Vegetable pulao pairs wonderfully with:\n\n"
                "1. **Cucumber & Mint Raita:** Whisk 1 cup chilled yogurt with grated cucumber, roasted cumin powder, black salt, and chopped mint.\n"
                "2. **Boondi Raita:** Crisp chickpea pearls soaked in seasoned yogurt.\n"
                "3. **Mirchi ka Salan:** Traditional tangy peanut and sesame gravy.\n"
                "4. **Roasted Papad & Mango Pickle:** Fast, classic crunch and spice."
            )
        elif last_dish in ("chapati", "roti", "paratha"):
            return (
                f"### Best Pairings for {last_title}\n\n"
                "These flatbreads go great with:\n"
                "1. **Dal Tadka or Dal Makhani** for a wholesome high-protein meal.\n"
                "2. **Paneer Tikka Masala** or mixed vegetable kurma.\n"
                "3. **Fresh plain curd (dahi)** and homemade lime or mango pickle."
            )

    # Adding ingredients (e.g. paneer, tofu, chicken)
    if any(k in prompt_lower for k in ["add paneer", "can i add paneer", "with paneer"]):
        return (
            f"### Adding Paneer to {last_title}\n\n"
            "Yes, paneer makes a great addition!\n"
            "- Cut paneer into 1/2-inch cubes.\n"
            "- Lightly pan-fry them in 1 tsp ghee for 2 minutes until light golden.\n"
            "- Gently fold the paneer into the dish in the final cooking stage so it stays soft and doesn't crumble."
        )

    # Storage and shelf-life
    if any(k in prompt_lower for k in ["store this", "keep this", "how long", "leftover", "reheat", "freeze"]):
        return (
            f"### Storage & Reheating for {last_title}\n\n"
            "- **Refrigeration:** Cool to room temperature and store in an airtight container within 2 hours. Keeps fresh for **2–3 days**.\n"
            "- **Freezing:** Can be frozen for up to 1 month. Thaw overnight in the fridge before reheating.\n"
            "- **Reheating:** Sprinkle 1–2 tbsp water over the dish and reheat covered on the stovetop or in a microwave to restore moisture."
        )

    return None


def _detect_intent(prompt_lower: str, ingredients: list, context: dict = None) -> str:
    """
    Classify the user's request into one of:
      'followup', 'technique', 'substitution', 'storage', 'recipe_request'
    """
    # Follow-up signals when context exists
    if context and context.get("last_dish"):
        followup_signals = [
            "this", "it", "cooker", "whistle", "whistles", "instead", "serve with",
            "side dish", "reheat", "can i add", "how long will", "leftover", "pressure"
        ]
        if any(s in prompt_lower for s in followup_signals):
            return "followup"

    # Substitution signals take priority – they're very specific
    substitution_signals = [
        "substitute", "substitution", "instead of", "replace", "replacement",
        "don't have", "do not have", "i have no", "without", "alternative to",
        "can i use", "what can i use", "what else can i use",
        "i ran out of", "ran out",
    ]
    for s in substitution_signals:
        if s in prompt_lower:
            return "substitution"

    # Storage signals
    storage_signals = [
        "store", "storage", "how long", "shelf life", "keep fresh",
        "refrigerate", "freeze", "how to preserve",
    ]
    for s in storage_signals:
        if s in prompt_lower:
            return "storage"

    # Technique signals – BUT only if no known dish/food name is present
    known_dish_words = [
        "pulao", "pulav", "biryani", "dal", "curry", "sabzi", "paratha",
        "upma", "poha", "dosa", "idli", "sambar", "khichdi", "halwa",
        "pasta", "pizza", "stew", "salad", "soup", "sandwich", "omelette",
        "pancake", "smoothie", "cake", "cookie", "bread", "stir fry", "fried rice",
        "shakshuka", "tofu", "noodle", "risotto", "paella",
    ]
    has_dish_name = any(dish in prompt_lower for dish in known_dish_words)

    # These technique signals are always technique regardless of dish name
    unconditional_technique = [
        "why is my", "why does my", "why are my",
        "becomes hard", "become hard", "gets hard", "turns hard",
        "becomes soft", "too hard", "too soft", "too dry", "too sticky",
        "fluffy egg", "perfect egg",
        "rice sticky", "rice mushy", "mushy rice", "sticky rice",
    ]
    for s in unconditional_technique:
        if s in prompt_lower:
            return "technique"

    # Conditional technique signals – only trigger when no specific dish name detected
    conditional_technique = [
        "how to make", "how do i make", "how do you make",
        "how to cook", "how do i cook",
        "tips for", "technique", "method", "secret to",
        "what is the best way", "what's the best way",
    ]
    if not has_dish_name:
        for s in conditional_technique:
            if s in prompt_lower:
                return "technique"

    return "recipe_request"


def _handle_technique_query(prompt_lower: str) -> str | None:
    """Return a canned answer for known technique questions, or None."""
    if any(k in prompt_lower for k in ["chapati", "roti", "phulka"]) and \
       any(k in prompt_lower for k in ["hard", "soft", "tough", "chewy", "stiff"]):
        return CULINARY_ADVICE_CATALOG["soft_chapati"]
    if any(k in prompt_lower for k in ["fluffy egg", "scramble", "perfect egg"]):
        return CULINARY_ADVICE_CATALOG["fluffy_eggs"]
    if any(k in prompt_lower for k in ["mushy rice", "sticky rice", "rice mushy", "rice sticky",
                                        "perfect rice", "fluffy rice", "cook rice"]):
        return CULINARY_ADVICE_CATALOG["rice_mushy"]
    return None


def _handle_substitution_query(prompt_lower: str, ingredients: list) -> str | None:
    """Return a canned answer for known substitution questions, or None."""
    if any(k in prompt_lower for k in ["substitute for egg", "egg substitute", "substitute eggs",
                                        "no egg", "replace egg", "without egg"]):
        return CULINARY_ADVICE_CATALOG["egg_substitution"]
    if any(k in prompt_lower for k in ["buttermilk", "substitute for milk"]):
        return CULINARY_ADVICE_CATALOG["buttermilk_substitution"]

    # Tomato substitution — general or curry-specific
    if any(k in prompt_lower for k in ["tomato", "tomatoes"]) and \
       any(k in prompt_lower for k in ["substitute", "instead", "replace", "without", "no tomato",
                                        "don't have", "do not have", "alternative"]):
        return CULINARY_ADVICE_CATALOG["tomato_substitute_curry"]
    return None


def _handle_storage_query(prompt_lower: str) -> str | None:
    if any(k in prompt_lower for k in ["store", "storage", "preserve", "how long", "shelf life",
                                        "refrigerate", "freeze", "keep fresh"]):
        return CULINARY_ADVICE_CATALOG["food_storage"]
    return None


def _score_recipes(prompt_tokens: set, ingredient_tokens: set, cuisine: str, max_time_min, dietary_restrictions: list) -> list:
    """
    Score every catalog recipe. Prompt keywords have high weight (+12) so explicit
    user requests override pre-filled ambient pantry ingredients (+2).
    """
    scored = []
    for r in EXPANDED_RECIPE_CATALOG:
        score = 0
        for kw in r["matching_keywords"]:
            if kw in prompt_tokens or any(kw in t for t in prompt_tokens):
                score += 12
            elif kw in ingredient_tokens or any(kw in t for t in ingredient_tokens):
                score += 2

        if cuisine and cuisine.lower() in r["cuisine"].lower():
            score += 10
        elif any(r["cuisine"].lower() in t for t in prompt_tokens):
            score += 8

        if max_time_min and r["total_time_min"] <= int(max_time_min):
            score += 4

        if dietary_restrictions:
            for d in dietary_restrictions:
                if any(d.lower() in tag.lower() for tag in r["dietary_tags"]):
                    score += 5

        scored.append((score, r))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def _build_recipe_reply(recipe: dict, ingredients: list) -> str:
    intro = f"Here is a recipe for **{recipe['title']}**."
    if ingredients:
        matched_ing = [i for i in ingredients
                       if any(kw in i.lower() for kw in recipe["matching_keywords"])]
        if matched_ing:
            intro += f" It uses your **{', '.join(matched_ing)}**!"

    return (
        f"{intro}\n\n"
        f"**Cuisine**: {recipe['cuisine']} | **Time**: ~{recipe['total_time_min']} mins | "
        f"**Difficulty**: {recipe['difficulty']} | **Servings**: {recipe['servings']}\n"
        f"**Calories**: ~{recipe['calories_per_serving']} kcal per serving | "
        f"{', '.join(recipe['dietary_tags'])}\n\n"
        f"### Description\n{recipe['description']}\n\n"
        f"### Ingredients\n"
        + "\n".join([f"- **{ing['quantity']}** — {ing['item']}" for ing in recipe["ingredients"]])
        + "\n\n"
        f"### Step-by-Step Instructions\n"
        + "\n".join([f"{i + 1}. {step}" for i, step in enumerate(recipe["instructions"])])
        + "\n\n"
        f"### Ingredient Substitutions\n"
        + "\n".join([f"- {sub}" for sub in recipe["substitutions"]])
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_cooking_assistant_response(
    user_prompt: str,
    ingredients: list = None,
    cuisine: str = None,
    max_time_min: int = None,
    skill_level: str = None,
    dietary_restrictions: list = None,
    conversation_history: list = None
) -> dict:
    """
    Handles user chat query for recipe ideas, cooking advice, and pantry ingredient matches.
    Priority order:
      1. Live Gemini text AI (if API key configured) — uses conversation history
         If API is configured but fails, return a clear error indicating the failure.
      2. Intent-aware heuristic knowledge base (offline demo mode):
         a. Follow-up queries (using conversation context)
         b. Technique questions → technique advice
         c. Substitution questions → substitution advice
         d. Storage questions → storage advice
         e. Recipe requests → scored catalog match
    """
    ingredients = ingredients or []
    dietary_restrictions = dietary_restrictions or []
    conversation_history = conversation_history or []
    user_prompt_clean = (user_prompt or "").strip()
    prompt_lower = user_prompt_clean.lower()

    # ── 1. Live Gemini AI path ──────────────────────────────────────────────
    api_key = get_ai_api_key()
    if api_key:
        system_instruction = (
            "You are Food Verse AI's Smart Cooking Assistant — an expert culinary guide specialising in "
            "practical, home-kitchen cooking for all skill levels, with strong knowledge of Indian, "
            "Mediterranean, Asian, Italian, and American cuisines.\n\n"
            "Your responsibilities:\n"
            "- Answer cooking questions directly, accurately, and helpfully.\n"
            "- When asked for a recipe, always provide: ingredient list with exact quantities, "
            "  preparation time, cooking time, clear numbered step-by-step instructions, and "
            "  at least one ingredient substitution tip.\n"
            "- When asked about a cooking technique (e.g. 'how to make chapati soft'), explain "
            "  the method clearly with the specific reason behind each tip.\n"
            "- When asked for ingredient substitutions, list 3–5 practical alternatives with "
            "  the correct quantity equivalent.\n"
            "- Respect dietary restrictions strictly — do not suggest ingredients the user has excluded.\n"
            "- If the user mentions they are cooking for a specific number of people, scale accordingly.\n"
            "- Ask one short clarifying question only if essential information is truly missing.\n"
            "- Never invent nutritional values or make unsupported health claims.\n"
            "- Keep answers concise but complete. Use markdown headers and bullet points for readability.\n"
            "- When the user follows up on a previous recipe or question, remember the context from "
            "  the conversation history and answer directly without re-introducing yourself."
        )

        # Contextual prompt enrichment if ambient filters were provided
        enriched_prompt = user_prompt_clean
        extra_context = []
        if ingredients:
            extra_context.append(f"Pantry ingredients available: {', '.join(ingredients)}")
        if cuisine:
            extra_context.append(f"Preferred cuisine: {cuisine}")
        if max_time_min:
            extra_context.append(f"Time limit: {max_time_min} minutes")
        if dietary_restrictions:
            extra_context.append(f"Dietary restrictions: {', '.join(dietary_restrictions)}")

        if extra_context:
            enriched_prompt += "\n\n[Additional Context: " + "; ".join(extra_context) + "]"

        ai_res = call_gemini_text(
            prompt=enriched_prompt,
            system_instruction=system_instruction,
            conversation_history=conversation_history
        )

        if ai_res.get("success") and ai_res.get("text", "").strip():
            return {
                "reply_text": ai_res["text"].strip(),
                "matched_recipes": [],
                "is_demo": False,
                "provider": ai_res.get("provider", "Google Gemini AI")
            }
        else:
            # API key is configured, but the model call failed. Return clear error!
            error_msg = ai_res.get("error", "Unknown API error")
            return {
                "reply_text": (
                    f"⚠️ **AI Service Unavailable**: The configured Gemini AI model could not process your request.\n\n"
                    f"**Details**: {error_msg}\n\n"
                    f"Please check your `GEMINI_API_KEY` and quota in `backend/.env`. "
                    f"To use the offline Smart Knowledge Base instead, remove the API key."
                ),
                "matched_recipes": [],
                "is_demo": False,
                "provider": "Google Gemini AI (Unavailable)"
            }

    # ── 2. Intent-aware heuristic knowledge base (offline demo mode) ─────────
    DEMO_PROVIDER = "Smart Culinary Knowledge Base (Demo Mode)"

    context = _extract_conversation_context(conversation_history)
    intent = _detect_intent(prompt_lower, ingredients, context)

    # 2a. Follow-up queries based on conversation history
    if intent == "followup":
        followup_ans = _handle_followup_query(prompt_lower, context)
        if followup_ans:
            return {
                "reply_text": followup_ans,
                "matched_recipes": [],
                "is_demo": True,
                "provider": DEMO_PROVIDER
            }

    # 2b. Technique questions
    if intent == "technique":
        answer = _handle_technique_query(prompt_lower)
        if answer:
            return {
                "reply_text": answer,
                "matched_recipes": [],
                "is_demo": True,
                "provider": DEMO_PROVIDER
            }
        return {
            "reply_text": (
                "That's a great cooking question! Here are key culinary techniques for better results:\n\n"
                "- **Prep first (Mise en place)**: Measure and chop all ingredients before turning on the heat.\n"
                "- **Control temperature**: High heat sears; gentle low-medium heat cooks through without drying.\n"
                "- **Resting**: Resting dough, roasted proteins, or grains lets moisture redistribute evenly.\n\n"
                "Could you tell me the specific dish or technique you'd like guidance on? I'll give you exact instructions!"
            ),
            "matched_recipes": [],
            "is_demo": True,
            "provider": DEMO_PROVIDER
        }

    # 2c. Substitution questions
    if intent == "substitution":
        answer = _handle_substitution_query(prompt_lower, ingredients)
        if answer:
            return {
                "reply_text": answer,
                "matched_recipes": [],
                "is_demo": True,
                "provider": DEMO_PROVIDER
            }
        return {
            "reply_text": (
                "For most ingredient substitutions, consider what culinary role the ingredient plays:\n\n"
                "- **Acidity (tomatoes, lemon)** → Plain yogurt (dahi), tamarind paste, amchur, or apple cider vinegar\n"
                "- **Creaminess (heavy cream, coconut milk)** → Blended cashew paste, plain yogurt, or silken tofu\n"
                "- **Umami / Savory depth (soy sauce, stock)** → Miso paste, mushroom broth, or nutritional yeast\n"
                "- **Binding (eggs in baking)** → Flax egg (1 tbsp ground flax + 3 tbsp warm water) or unsweetened applesauce\n\n"
                "Tell me the specific ingredient and dish you are cooking, and I'll give you the exact substitute and ratio!"
            ),
            "matched_recipes": [],
            "is_demo": True,
            "provider": DEMO_PROVIDER
        }

    # 2d. Storage questions
    if intent == "storage":
        answer = _handle_storage_query(prompt_lower)
        if answer:
            return {
                "reply_text": answer,
                "matched_recipes": [],
                "is_demo": True,
                "provider": DEMO_PROVIDER
            }

    # 2e. Recipe request — scored catalog match with prompt prioritization
    prompt_words = re.findall(r"\b\w+\b", prompt_lower)
    prompt_tokens = set(w.strip() for w in prompt_words if len(w.strip()) > 2)

    ing_words = [re.sub(r"[^\w\s]", "", i.lower()).strip() for i in ingredients]
    ingredient_tokens = set(w for w in ing_words if len(w) > 2)

    scored = _score_recipes(prompt_tokens, ingredient_tokens, cuisine, max_time_min, dietary_restrictions)
    best_score, best_recipe = scored[0]

    # If best score is 0, ask a clarifying question
    if best_score == 0:
        return {
            "reply_text": (
                "I'd love to help you cook something delicious! To give you the best recipe, could you share:\n\n"
                "1. **What ingredients** you have on hand?\n"
                "2. **How much time** you'd like to spend? (e.g. 15 min, 30 min)\n"
                "3. **Any dietary preferences?** (Vegetarian, Vegan, Gluten-Free, etc.)\n"
                "4. **Cuisine preference?** (Indian, Italian, Asian, Mediterranean, American)\n\n"
                "Or simply ask: *'How do I make vegetable pulao for 2 people?'*"
            ),
            "matched_recipes": [],
            "is_demo": True,
            "provider": DEMO_PROVIDER
        }

    return {
        "reply_text": _build_recipe_reply(best_recipe, ingredients),
        "matched_recipes": [best_recipe],
        "is_demo": True,
        "provider": DEMO_PROVIDER
    }
