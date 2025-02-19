# Use the official Miniconda3 image as the base image.
FROM docker.io/continuumio/miniconda3

# Install Python 3.11, tomopy, and dxchange from conda-forge.
RUN conda install -y -c conda-forge python=3.11 tomopy dxchange

# Install globus-compute-sdk via pip.
RUN pip install --no-cache-dir globus-compute-sdk

# Set the working directory.
WORKDIR /app

# (Optional) Copy your application code into the container.
# COPY . /app

# Default command: launch an interactive Python shell.
CMD ["python3"]
