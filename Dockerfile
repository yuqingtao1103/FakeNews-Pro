FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY models ./models
COPY data ./data
ENV MODEL_PATH=models/baseline_tfidf_lr.joblib FRONTEND_ORIGIN=* RATE_LIMIT_PER_MIN=30
EXPOSE 10000
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "10000"]
