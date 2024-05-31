# Preferentially Sampled Personal Weather Stations
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11405961.svg)](https://doi.org/10.5281/zenodo.11405961)

This repository contains all of the data and code used for analyzing preferential sampling in personal weather stations.

# Organization
* preprocessed_data: this folder contains the preprocessed data with weather underground and census data combined into .shp files, organized by location / time period.
* notebooks: this folder contains .ipynb notebooks used for conducting analysis.

Please consult the notebooks to see the code used in the analysis.

# Running code
The following requirements are needed to run the code in this repository.
* PyMC - for running models.
* Arviz - for visualizing PyMC results.
* GDAL - must be installed for data preprocessing steps.
* PySAL - for geographic data manipulation.
* Geopandas - for working with .shp files.
* Statsmodels - for some basic statistical analysis.
* Numpy and Pandas - for basic data manipulation.

If you would like to understand how to pull Weather Underground data, or better understand any of the questions, please make an issue, or send me a note! I would love to hear your questions.
