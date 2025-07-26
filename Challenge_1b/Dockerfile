# Dockerfile for Challenge 1b: Multi-Collection PDF Analysis
# Adobe India Hackathon 2025

FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main processing script
COPY process_challenge1b.py .

# Copy collection directories with their structure
COPY "Collection 1/" "Collection 1/"
COPY "Collection 2/" "Collection 2/"
COPY "Collection 3/" "Collection 3/"

# Set environment variables for optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Command to run when container starts
CMD ["python", "process_challenge1b.py"]
