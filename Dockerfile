FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser
USER appuser

EXPOSE 7860

<<<<<<< HEAD
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
=======
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
  CMD curl -f http://localhost:7860/health || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
