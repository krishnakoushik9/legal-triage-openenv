FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for some python packages and healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything and ensure appuser ownership
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 7860

# Robust healthcheck using python's built-in urllib
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')" || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
