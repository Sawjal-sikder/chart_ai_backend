# Use Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies for OpenCV and OCR libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgdal-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-dev \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django port
EXPOSE 14006


# Run Django development server
CMD ["uvicorn", "Server.main:app", "--host", "0.0.0.0", "--port", "14006"]