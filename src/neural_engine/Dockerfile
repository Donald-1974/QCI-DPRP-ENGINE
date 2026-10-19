# Use an optimized, lightweight Python 3.10 base image
FROM python:3.10-slim

# Set the working directory within the container
WORKDIR /app

# Install system-level dependencies required for heavy math libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core architecture into the container
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY run_engine.py /app/

# Grant execution permissions to the MLOps entrypoint script
RUN chmod +x /app/scripts/retrain_model.sh

# Set environment variables for optimal tensor computation
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

# Define the default command when the container launches
ENTRYPOINT ["/app/scripts/retrain_model.sh"]
