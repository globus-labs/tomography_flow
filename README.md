# Tomography Flow Example

![An example IRI flow for tomography](img/lightsources.png "Tomography IRI")

This repository demonstrates how [Tomopy](https://tomopy.readthedocs.io/en/latest/) reconstructions can be automated using [Globus Flows](https://www.globus.org/globus-flows-service). The notebook aims to show how an individual flow can be used to integrate different light sources and compute facilities.

## Configuring a compute environment

We use [Globus Compute](https://globus-compute.readthedocs.io/en/latest/index.html) to perform Tomopy remotely. To plug your own Compute endpoint in you will need to install globus-compute-endpoint and the tomopy dependencies listed in compute-requirements.txt



# tomography_flow Container

This repository, `tomography_flow`, provides an OCI recipe for building a container image designed for tomographic data processing. The container installs:

- **tomopy** – For tomographic reconstruction (installed from conda-forge)
- **dxchange** – For data exchange utilities (installed from conda-forge)
- **globus-compute-sdk** – For interacting with Globus Compute (installed via pip)

It also includes a script, `run_tomopy.py`, which performs a complete tomographic reconstruction workflow.

## Repository Structure

tomography_flow/ 
├── recipes/ 
│ └── Dockerfile # OCI recipe for building the container image 
├── run_tomopy.py # Script to run the tomographic reconstruction workflow 
├── tomography_flow/ # Package containing the tomo_flow module (with recon.py, etc.) 
└── README.md # This file

## Prerequisites

- **Podman**: Ensure Podman is installed.
    ```bash
    sudo apt-get update && sudo apt-get install podman
    ```
- **Git**: To clone the repository.
- **Miniconda3**: The container uses conda to install packages from conda-forge.

## Building the Container Image

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/tomography_flow.git
   cd tomography_flow