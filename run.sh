#!/bin/bash


# 1. Activate venv
source venv/bin/activate

# 2. Install new dependencies (this will download torch & transformers)
# Step 1: Install CPU‑only PyTorch (150 MB, no NVIDIA)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Step 2: Install everything else (these will *not* re-download torch)
pip install pandas scikit-learn joblib jupyter numpy fastapi uvicorn pydantic python-multipart transformers accelerate sentence-transformers

# 3. Run the training script (downloads DistilBERT during first run)
python brain.py

# 4. Test the API (if you have the API code ready)
uvicorn api.main:app --host 0.0.0.0 --port 8000


# SETUP UI

# Install dependencies
pnpm install axios react-router-dom jwt-decode
pnpm install -D @types/node @types/react-router-dom tailwindcss postcss autoprefixer

# Initialize Tailwind CSS
npx tailwindcss init -p