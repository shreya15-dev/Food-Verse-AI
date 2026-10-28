import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "foodverse.db"
TEMP_UPLOAD_DIR = BASE_DIR / "temp_uploads"
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)

# Load .env file if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                clean_key = key.strip()
                clean_val = val.strip().strip("'\"")
                if clean_val or clean_key not in os.environ:
                    os.environ[clean_key] = clean_val
# Load .env file — check backend/ first, then project root as fallback
def _load_env_file(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    clean_key = key.strip()
                    clean_val = val.strip().strip("'\"")
                    if clean_val or clean_key not in os.environ:
                        os.environ[clean_key] = clean_val
        return True
    return False

# Try backend/.env first, then smartbridge/.env (project root)
if not _load_env_file(BASE_DIR / ".env"):
    _load_env_file(BASE_DIR.parent / ".env")

# AI Configuration - supports GEMINI_API_KEY, AI_API_KEY, and GOOGLE_API_KEY
def get_ai_api_key() -> str:
    return (
        os.environ.get("GEMINI_API_KEY", "").strip()
        or os.environ.get("AI_API_KEY", "").strip()
        or os.environ.get("GOOGLE_API_KEY", "").strip()
    )

GEMINI_API_KEY = get_ai_api_key()
IS_AI_CONFIGURED = bool(GEMINI_API_KEY)

# Upload constraints
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "avi"}
MAX_CONTENT_LENGTH = 45 * 1024 * 1024  # 45 MB max request size
MAX_IMAGE_SIZE = 15 * 1024 * 1024      # 15 MB image limit
MAX_VIDEO_SIZE = 35 * 1024 * 1024      # 35 MB video limit

def is_allowed_file(filename: str, allowed_set: set) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed_set
