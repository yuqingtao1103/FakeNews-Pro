FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
RUN mkdir -p models data/processed data/feedback

ENV MODEL_PATH=models/baseline_tfidf_lr.joblib
ENV FRONTEND_ORIGIN=*
ENV RATE_LIMIT_PER_MIN=30

EXPOSE 10000
CMD ["uvicorn","src.api.app:app","--host","0.0.0.0","--port","10000"]
