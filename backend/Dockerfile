# Use a slim base image
FROM python:3.10.6-slim-bullseye

WORKDIR /app

# Install necessary system dependencies, including build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    unzip \
    ffmpeg \
    libsndfile1 \
    build-essential \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt for caching purposes
COPY requirements.txt .
COPY lerobot /data/lerobot

# Upgrade pip and install Python dependencies
# Notice that we install faster-whisper instead of whispercpp
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -e "/data/lerobot[feetech]" && \
    python3 -m pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Copy the rest of the application code into the container
COPY . /app

# Specify the startup command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Expose port 8000
EXPOSE 8000
