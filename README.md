# Preferentially Sampled Personal Weather Stations
This repository contains all of the code used for analyzing preferential sampling in personal weather stations.

The repository is organized into the following directories:
* Preprocessing: this folder contains .ipynb notebooks used for preproccesing data.
* Analysis: this folder contains .ipynb notebooks used for conducting analysis.
* Data: this folder contains both raw and preprocessed data. At this time, this directory is ignored by git (using the .gitignore file). This is to avoid sending too much data to github.

Please consult each of these directories to read more about the scripts contained within them.

# Running code
We created this environment using conda. As such, you can find the conda requirements in the environment.yaml file.

Package requirements include:
* PyMC - for running models
* GDAL - must be installed for data preprocessing steps
* PySAL