import io
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import unittest
from PIL import Image
from app import app
import database

class FoodVerseApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def create_dummy_image(self, color=(100, 180, 80)):
        """Creates an in-memory PNG image for testing uploads."""
        file_obj = io.BytesIO()
        img = Image.new("RGB", (200, 200), color=color)
        img.save(file_obj, format="PNG")
        file_obj.seek(0)
        return file_obj

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("ai_configured", data)
        self.assertIn("supported_modules", data)

    def test_food_analysis_endpoint(self):
        img_bytes = self.create_dummy_image((50, 150, 50))
        response = self.client.post(
            "/api/analyze/food",
            data={"image": (img_bytes, "fresh_salad_bowl.png")},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        self.assertIn("food_name", res_json["data"])
        self.assertIn("calories", res_json["data"])
        self.assertIn("protein_g", res_json["data"])
        self.assertIn("disclaimer", res_json["data"])

    def test_freshness_analysis_endpoint(self):
        img_bytes = self.create_dummy_image((200, 50, 50))
        response = self.client.post(
            "/api/analyze/freshness",
            data={"image": (img_bytes, "ripe_apple.png")},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        self.assertIn("freshness_score", res_json["data"])
        self.assertIn("category", res_json["data"])
        self.assertIn("observations", res_json["data"])

    def test_hygiene_analysis_endpoint(self):
        img_bytes = self.create_dummy_image((210, 210, 210))
        response = self.client.post(
            "/api/analyze/hygiene",
            data={"media": (img_bytes, "prep_station.png")},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        self.assertIn("hygiene_score", res_json["data"])
        self.assertIn("observations", res_json["data"])

    def test_video_hygiene_analysis_endpoint(self):
        video_sample = Path(__file__).resolve().parent.parent.parent / "sample_media" / "kitchen_audit_walkthrough.mp4"
        if video_sample.exists():
            with open(video_sample, "rb") as vf:
                response = self.client.post(
                    "/api/analyze/hygiene",
                    data={"media": (vf, "kitchen_audit_walkthrough.mp4")},
                    content_type="multipart/form-data"
                )
                self.assertEqual(response.status_code, 200)
                res_json = response.get_json()
                self.assertTrue(res_json["success"])
                self.assertTrue(res_json["data"]["is_video"])
                self.assertIn("keyframes", res_json["data"])
                self.assertGreater(len(res_json["data"]["keyframes"]), 0)

    def test_cooking_assistant_chat(self):
        response = self.client.post(
            "/api/recipes/chat",
            json={
                "prompt": "I want a quick dinner with eggs and tomatoes",
                "ingredients": ["eggs", "tomatoes", "garlic"],
                "cuisine": "Mediterranean"
            }
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        self.assertIn("reply_text", res_json["data"])

    def test_cooking_assistant_recipe_pulao(self):
        response = self.client.post(
            "/api/recipes/chat",
            json={
                "prompt": "How do I make vegetable pulao for two people? Give exact ingredient quantities and steps.",
                "ingredients": []
            }
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        reply = res_json["data"]["reply_text"].lower()
        self.assertIn("pulao", reply)
        self.assertIn("basmati rice", reply)

    def test_cooking_assistant_tomato_substitution(self):
        response = self.client.post(
            "/api/recipes/chat",
            json={
                "prompt": "I do not have tomatoes. What can I use instead in paneer curry?",
                "ingredients": ["paneer", "onion", "cream", "spices"]
            }
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        reply = res_json["data"]["reply_text"].lower()
        self.assertTrue("substitute" in reply or "yogurt" in reply or "dahi" in reply)

    def test_cooking_assistant_soft_chapati_technique(self):
        response = self.client.post(
            "/api/recipes/chat",
            json={
                "prompt": "My chapati becomes hard after cooking. How can I make it soft?",
                "ingredients": []
            }
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        reply = res_json["data"]["reply_text"].lower()
        self.assertIn("chapati", reply)
        self.assertTrue("soft" in reply and "dough" in reply)

    def test_cooking_assistant_quick_veg_breakfast(self):
        response = self.client.post(
            "/api/recipes/chat",
            json={
                "prompt": "Give me a simple vegetarian breakfast recipe that takes 15 minutes.",
                "ingredients": [],
                "max_time_min": 15,
                "dietary_restrictions": ["Vegetarian"]
            }
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        reply = res_json["data"]["reply_text"].lower()
        self.assertTrue("upma" in reply or "poha" in reply or "15" in reply)

    def test_cooking_assistant_followup_context(self):
        hist = [
            {"role": "user", "text": "How do I make vegetable pulao for two people? Give exact ingredient quantities and steps."},
            {"role": "assistant", "text": "Here is a recipe for Fragrant Vegetable Pulao (Serves 2)..."}
        ]
        response = self.client.post(
            "/api/recipes/chat",
            json={
                "prompt": "Can I make this in a pressure cooker instead? How many whistles?",
                "conversation_history": hist
            }
        )
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        reply = res_json["data"]["reply_text"].lower()
        self.assertTrue("pressure cooker" in reply or "whistle" in reply)

    def test_food_analysis_with_real_sample(self):
        sample_path = Path(__file__).resolve().parent.parent.parent / "sample_media" / "food_grilled_chicken.jpg"
        if sample_path.exists():
            with open(sample_path, "rb") as f:
                response = self.client.post(
                    "/api/analyze/food",
                    data={"image": (f, "food_grilled_chicken.jpg")},
                    content_type="multipart/form-data"
                )
                self.assertEqual(response.status_code, 200)
                res_json = response.get_json()
                self.assertTrue(res_json["success"])
                self.assertIn("food_name", res_json["data"])
                self.assertGreater(res_json["data"]["calories"], 0)

    def test_meal_planner_generation(self):
        profile = {
            "age": 28,
            "weight_kg": 72,
            "height_cm": 175,
            "gender": "male",
            "activity_level": "moderately_active",
            "dietary_preference": "Vegetarian",
            "goal": "healthy_weight_loss",
            "meal_frequency": "3_meals_1_snack",
            "allergies": ["Peanuts"]
        }
        response = self.client.post("/api/meal-plan/generate", json=profile)
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertTrue(res_json["success"])
        self.assertIn("schedule", res_json["data"])
        self.assertEqual(len(res_json["data"]["schedule"]), 7)
        self.assertIn("grocery_list", res_json["data"])

    def test_history_flow(self):
        # Fetch history
        res = self.client.get("/api/history")
        self.assertEqual(res.status_code, 200)
        history_items = res.get_json()["data"]
        self.assertIsInstance(history_items, list)

if __name__ == "__main__":
    unittest.main()
