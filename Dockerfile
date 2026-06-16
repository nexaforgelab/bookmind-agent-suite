FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 系统依赖（OCR/PDF 渲染需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng \
        libmupdf-dev \
        libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

VOLUME ["/app/data", "/app/reports"]
WORKDIR /app

ENTRYPOINT ["python", "-m", "bookmind.cli"]
CMD ["doctor"]
