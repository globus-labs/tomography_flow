# Tomography Flow Example

![An example IRI flow for tomography](img/lightsources.png "Tomography IRI")

This repository demonstrates how [Tomopy](https://tomopy.readthedocs.io/en/latest/) reconstructions can be automated using [Globus Flows](https://www.globus.org/globus-flows-service). The notebook aims to show how an individual flow can be used to integrate different light sources and compute facilities.

## Configuring a compute environment

We use [Globus Compute](https://globus-compute.readthedocs.io/en/latest/index.html) to perform Tomopy remotely. To plug your own Compute endpoint in you will need to install globus-compute-endpoint and the tomopy dependencies listed in compute-requirements.txt


