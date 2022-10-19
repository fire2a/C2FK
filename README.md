# C2F+K: A new open-source wildfire simulator for Chile
## Jaime Carrasco, Cristóbal Pais, David Palacios, Felipe Soto, Rodrigo Mahaluf, Horacio Gilabert, Alejandro Miranda, Gabriela Alfaro, Miguel Castillo, and Andrés Weintraub

# Disclaimer
This software is for research use only. There is no warranty of any kind; there is not even the implied warranty of fitness for use.

# Introduction
Wildfire spatial simulation has proven to be a useful tool for fire management, both for preventive planning and suppression. However, these tools are not always publicly available, and those that exist require restrictive/limited licenses or belong to private companies or government institutions. In this repository, we present an open-source computational tool to simulate the growth of fires that can occur in any region of Chile, and has the potential to estimate burn probability maps which requires an iterative and concatenated process of spatially explicit simulation of fire ignition, and fire growth scenarios. This system -- C2F+K -- is based on the Cell2Fire simulator and the Chilean fire behavior system, KITRAL. Our implementation proposes new equations for the calculation of the rate of spread and length-to-breadth ratio as a function of wind speed, based on an elliptical shape model; we also incorporate a model of crown fire behavior validated with numerical experiments. We illustrate its performance comparing it to real and simulated wildfires using the KITRAL software. C2F+K features cross-platform compatibility and flexibility, which allows taking advantage of parallel computing in fire growth modeling and generating risk maps from multiple stochastic simulations.

# Installation
Installation may require some familiarity with C++, make, and Python.
* cd C2FK/Cell2FireC
* (edit Makefile to have the correct path to Eigen)
* make
* cd .. 
* pip install -r requirements.txt

# Requirements
- Boost (C++)
- Eigen (C++)
- Python 3.6
- numpy
- pandas
- matplotlib
- seaborn
- tqdm
- rasterio
- networkx (for stats module)

# Illustrative examples
A tutorial can be found at [C2F+K Tutorial](https://docs.google.com/presentation/d/1Y6fPAhDrSThGSvYFvqdccXTvVrUcvbHZsDLAwbfMD18/edit?usp=sharing)
