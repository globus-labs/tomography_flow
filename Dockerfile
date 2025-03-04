# Use the fully qualified Miniconda3 image from Docker Hub.
FROM docker.io/continuumio/miniconda3

# Install Python 3.11, tomopy, dxchange, and matplotlib from conda-forge.
RUN conda install -y -c conda-forge python=3.11 tomopy dxchange matplotlib && \
    conda clean -afy

# Install globus-compute-sdk via pip.
RUN pip install --no-cache-dir globus-compute-sdk

# Set the maximum number of threads for NumExpr.
ENV NUMEXPR_MAX_THREADS=64

# Set the working directory.
WORKDIR /app

# (Optional) Copy your application code into the container.
# COPY . /app

# Default command: launch an interactive Python shell.
CMD ["python3"]