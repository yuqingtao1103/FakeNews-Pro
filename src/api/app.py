import os, time, json, pathlib, subprocess
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from src.models.inference import BaselineModel
from src.api.schemas import PredictIn, PredictOut, FeedbackIn

MODEL_PATH = os.getenv("MODEL_PATH", "models/baseline_tfidf_lr.joblib")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "30"))

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Fake News API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(status_code=429, content={"detail":"Too many requests. Please slow down."}))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN] if FRONTEND_ORIGIN != "*" else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-train tiny model if missing
if not pathlib.Path(MODEL_PATH).exists():
    pathlib.Path("models").mkdir(parents=True, exist_ok=True)
    subprocess.run(["python", "-m", "src.data.prepare", "--out", "data/processed"], check=True)
    subprocess.run(["python","-m","src.models.train_baseline","--train","data/processed/train.parquet","--val","data/processed/val.parquet","--out",MODEL_PATH], check=True)

model = BaselineModel(MODEL_PATH)

@app.get("/health")
def health():
    return {"ok": True, "model": os.path.basename(MODEL_PATH), "rate_limit_per_min": RATE_LIMIT_PER_MIN}

@app.post("/predict", response_model=PredictOut)
@limiter.limit(f"{RATE_LIMIT_PER_MIN}/minute")
def predict(payload: PredictIn, request: Request):
    text_parts = [t for t in [payload.headline, payload.body] if t]
    if not text_parts:
        raise HTTPException(status_code=400, detail="Provide headline or body.")
    text = " ".join(text_parts).strip()
    if len(text) > 12000:
        raise HTTPException(status_code=413, detail="Text too long (max ~12k chars).")
    label, proba = model.predict(text)
    top_feats = model.top_features(text, k=10)
    return PredictOut(label=label, proba=proba, top_features=top_feats)

@app.post("/feedback")
def feedback(item: FeedbackIn):
    fb_dir = pathlib.Path("data/feedback"); fb_dir.mkdir(parents=True, exist_ok=True)
    path = fb_dir / f"fb_{int(time.time())}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item.model_dump(), f, ensure_ascii=False, indent=2)
    return {"saved": True}

from fastapi.responses import Response

# add this route near the others
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Silence the 404 by returning an empty 204
    return Response(status_code=204)

from ..models.inference import BaselineModel