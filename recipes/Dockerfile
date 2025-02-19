# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Install system dependencies needed for building Python packages (adjust as needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory (optional)
WORKDIR /app

# (Optional) Copy your application code into the container
# COPY . /app

# Install tomopy, dxchange, and Globus Compute SDK from PyPI
RUN pip install --no-cache-dir tomopy dxchange globus-compute-sdk

# Default command: launch an interactive Python shell
CMD ["python3"]
