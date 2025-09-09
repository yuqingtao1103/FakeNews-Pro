# Fake News Project (Zero → Deploy)

A production-style web app that detects potentially fake/misleading news using a classical baseline (TF‑IDF + Logistic Regression) with a clean React UI. Rate‑limiting, CORS, Docker deploy included.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.data.prepare --out data/processed
python -m src.models.train_baseline --train data/processed/train.parquet --val data/processed/val.parquet --out models/baseline_tfidf_lr.joblib

uvicorn src.api.app:app --port 8000 --reload

# Frontend
cd frontend && npm i && echo "VITE_API_BASE=http://localhost:8000" > .env && npm run dev
```
