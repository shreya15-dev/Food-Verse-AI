import os
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    MAX_IMAGE_SIZE,
    MAX_VIDEO_SIZE,
    MAX_CONTENT_LENGTH,
    IS_AI_CONFIGURED,
    TEMP_UPLOAD_DIR,
    is_allowed_file
)
import database
from services.nutrition_service import analyze_food_image
from services.freshness_service import analyze_freshness
from services.hygiene_service import analyze_kitchen_hygiene
from services.recipe_service import generate_cooking_assistant_response
from services.meal_planner_service import generate_weekly_meal_plan

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Enable CORS for frontend development
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = app.make_default_options_response()
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, x-requested-with"
        res.headers["Access-Control-Allow-Private-Network"] = "true"
        return res

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, x-requested-with"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        "success": False,
        "error": "The uploaded file exceeds the maximum permitted payload size.",
        "status_code": 413
    }), 413

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": "Bad request. Please verify submitted parameters.",
        "status_code": 400
    }), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": "An internal server error occurred while processing the request.",
        "status_code": 500
    }), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "app_name": "Food Verse AI API",
        "version": "1.0.0",
        "ai_configured": IS_AI_CONFIGURED,
        "mode": "Live Multimodal AI" if IS_AI_CONFIGURED else "Heuristic Simulation Demo Mode",
        "supported_modules": [
            "ai_food_recognition",
            "food_freshness_assessment",
            "restaurant_hygiene_monitoring",
            "smart_cooking_assistant",
            "personalized_meal_planner"
        ]
    })

@app.route("/api/analyze/food", methods=["POST"])
def analyze_food():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided in request."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected for upload."}), 400

    if not is_allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({
            "success": False,
            "error": f"Unsupported format. Allowed formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        }), 400

    safe_name = secure_filename(file.filename)
    temp_path = None
    try:
        # Create temp file securely
        with tempfile.NamedTemporaryFile(delete=False, suffix="_" + safe_name, dir=TEMP_UPLOAD_DIR) as temp_f:
            temp_path = temp_f.name
            file.save(temp_path)

        file_size = os.path.getsize(temp_path)
        if file_size > MAX_IMAGE_SIZE:
            return jsonify({"success": False, "error": "Image file exceeds 15 MB limit."}), 400

        result = analyze_food_image(temp_path, safe_name)
        
        # Save record to database history
        summary = f"{result.get('food_name')} - {result.get('calories')} kcal | {result.get('category')}"
        record_id = database.save_analysis(
            module_type="food",
            title=result.get("food_name", "Food Analysis"),
            summary=summary,
            data=result,
            is_demo=result.get("is_demo", True)
        )
        result["record_id"] = record_id

        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to analyze food image: {str(e)}"}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.route("/api/analyze/freshness", methods=["POST"])
def analyze_produce_freshness():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided in request."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected for upload."}), 400

    if not is_allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({
            "success": False,
            "error": f"Unsupported image format. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        }), 400

    safe_name = secure_filename(file.filename)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix="_" + safe_name, dir=TEMP_UPLOAD_DIR) as temp_f:
            temp_path = temp_f.name
            file.save(temp_path)

        file_size = os.path.getsize(temp_path)
        if file_size > MAX_IMAGE_SIZE:
            return jsonify({"success": False, "error": "Image file exceeds 15 MB limit."}), 400

        result = analyze_freshness(temp_path, safe_name)

        summary = f"{result.get('item_identified')} - {result.get('category')} (Score: {result.get('freshness_score')}/100)"
        record_id = database.save_analysis(
            module_type="freshness",
            title=f"Freshness: {result.get('item_identified', 'Produce')}",
            summary=summary,
            data=result,
            is_demo=result.get("is_demo", True)
        )
        result["record_id"] = record_id

        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to assess freshness: {str(e)}"}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.route("/api/analyze/hygiene", methods=["POST"])
def analyze_hygiene():
    if "media" not in request.files:
        return jsonify({"success": False, "error": "No kitchen media file (image or video) provided."}), 400

    file = request.files["media"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No media file selected for inspection."}), 400

    safe_name = secure_filename(file.filename)
    is_image = is_allowed_file(safe_name, ALLOWED_IMAGE_EXTENSIONS)
    is_video = is_allowed_file(safe_name, ALLOWED_VIDEO_EXTENSIONS)

    if not (is_image or is_video):
        return jsonify({
            "success": False,
            "error": "Unsupported file format. Please upload JPG, PNG, WEBP images or MP4, WEBM videos."
        }), 400

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix="_" + safe_name, dir=TEMP_UPLOAD_DIR) as temp_f:
            temp_path = temp_f.name
            file.save(temp_path)

        file_size = os.path.getsize(temp_path)
        max_limit = MAX_VIDEO_SIZE if is_video else MAX_IMAGE_SIZE
        if file_size > max_limit:
            return jsonify({
                "success": False,
                "error": f"File exceeds maximum allowed size ({round(max_limit / (1024*1024))} MB)."
            }), 400

        result = analyze_kitchen_hygiene(temp_path, safe_name, is_video=is_video)

        summary = f"{result.get('preliminary_grade')} - Score: {result.get('hygiene_score')}/100"
        record_id = database.save_analysis(
            module_type="hygiene",
            title=f"Hygiene Audit ({'Video' if is_video else 'Image'})",
            summary=summary,
            data=result,
            is_demo=result.get("is_demo", True)
        )
        result["record_id"] = record_id

        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": f"Hygiene analysis failed: {str(e)}"}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.route("/api/recipes/chat", methods=["POST"])
def cooking_assistant_chat():
    req_data = request.get_json(silent=True) or {}
    user_prompt = req_data.get("prompt", "")
    ingredients = req_data.get("ingredients", [])
    cuisine = req_data.get("cuisine", "")
    max_time_min = req_data.get("max_time_min")
    skill_level = req_data.get("skill_level")
    dietary_restrictions = req_data.get("dietary_restrictions", [])
    history = req_data.get("conversation_history", [])

    if not user_prompt and not ingredients:
        return jsonify({
            "success": False,
            "error": "Please enter a message or at least one ingredient to search recipes."
        }), 400

    try:
        response_data = generate_cooking_assistant_response(
            user_prompt=user_prompt,
            ingredients=ingredients,
            cuisine=cuisine,
            max_time_min=max_time_min,
            skill_level=skill_level,
            dietary_restrictions=dietary_restrictions,
            conversation_history=history
        )

        # Save record to database history
        matched = response_data.get("matched_recipes", [])
        top_recipe = matched[0] if matched else {}
        recipe_title = top_recipe.get("title", user_prompt[:40] if user_prompt else "Cooking Advice")
        summary = f"{recipe_title} - {top_recipe.get('prep_time', 'Quick')} | {top_recipe.get('cuisine', 'Culinary')}" if matched else (user_prompt[:60] if user_prompt else "Cooking Assistant Query")
        record_id = database.save_analysis(
            module_type="recipe",
            title=f"Recipe: {recipe_title}",
            summary=summary,
            data=response_data,
            is_demo=response_data.get("is_demo", True)
        )
        response_data["record_id"] = record_id

        return jsonify({"success": True, "data": response_data})
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to generate recipe response: {str(e)}"}), 500

@app.route("/api/meal-plan/generate", methods=["POST"])
def create_meal_plan():
    profile_data = request.get_json(silent=True) or {}
    
    # Input validation
    try:
        age = int(profile_data.get("age", 25))
        if age < 10 or age > 120:
            return jsonify({"success": False, "error": "Age must be between 10 and 120 years."}), 400
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid age format."}), 400

    try:
        plan = generate_weekly_meal_plan(profile_data)
        
        # Save to SQLite database
        database.save_user_profile(profile_data)
        plan_id = database.save_meal_plan(profile_data, plan)
        plan["plan_id"] = plan_id

        return jsonify({"success": True, "data": plan})
    except Exception as e:
        return jsonify({"success": False, "error": f"Meal plan generation failed: {str(e)}"}), 500

@app.route("/api/meal-plan/saved", methods=["GET"])
def get_saved_meal_plan():
    try:
        saved = database.get_latest_meal_plan()
        profile = database.get_user_profile()
        return jsonify({
            "success": True,
            "data": {
                "saved_plan": saved,
                "profile": profile
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/history", methods=["GET"])
def get_analysis_history():
    module_type = request.args.get("module_type")
    limit = request.args.get("limit", 50, type=int)
    try:
        items = database.get_history(limit=limit, module_type=module_type)
        return jsonify({"success": True, "data": items, "count": len(items)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/history/<int:record_id>", methods=["GET"])
def get_single_history(record_id: int):
    try:
        item = database.get_analysis_by_id(record_id)
        if not item:
            return jsonify({"success": False, "error": "History record not found."}), 404
        return jsonify({"success": True, "data": item})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/history/<int:record_id>", methods=["DELETE"])
def delete_single_history(record_id: int):
    try:
        deleted = database.delete_analysis(record_id)
        if not deleted:
            return jsonify({"success": False, "error": "Record not found or already deleted."}), 404
        return jsonify({"success": True, "message": "Record removed from history."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/history", methods=["DELETE"])
def clear_all_history():
    try:
        count = database.clear_history()
        return jsonify({"success": True, "message": f"Successfully cleared {count} records."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Food Verse AI backend server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
