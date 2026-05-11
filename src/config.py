# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
DATASET_DIR = BASE_DIR / "dataset"
PROMPTS_DIR = BASE_DIR / "prompts"
OUTPUTS_DIR = BASE_DIR / "outputs"
RESULTS_DIR = BASE_DIR / "results"

# API Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-lite"

# Tạo các folder nếu chưa tồn tại
for path in [OUTPUTS_DIR, RESULTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)
