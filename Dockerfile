FROM python:3.11-slim-bookworm

LABEL maintainer="BookMind Team"
LABEL description="BookMind Multi-Agent Reading Suite - Deep PDF book interpretation"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir faiss-cpu pytesseract ocrmypdf

# Copy application code
COPY . .

# Install bookmind package
RUN pip install -e .

# Create data directories
RUN mkdir -p /app/data /app/output /app/exports

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV BOOKMIND_DATA_DIR=/app/data
ENV BOOKMIND_OUTPUT_DIR=/app/output

# Expose port if needed (for future web interface)
EXPOSE 8000

# Default command
CMD ["bookmind", "--help"]
