# C2FK: New Extensions of Cell2Fire Software for Fire Risk Analysis and Evaluation in Chilean Forests
## Jaime Carrasco-Barra<sup>a,c,*</sup>, José Ramón González-Olabarria<sup>j</sup>, Camilo Matus-Olivares<sup>a</sup>,   Felipe Ulloa-Fierro<sup>d,e</sup>, Felipe Soto<sup>f</sup>, David Palacios<sup>c</sup>, Rodrigo Mahaluf<sup>c</sup>, Felipe de la Barra<sup>c</sup>,   Carolina Espinoza<sup>h</sup>, Matías Vilches<sup>c</sup>, Matilde Rivas<sup>c</sup>, Fernando Badilla<sup>c</sup>, Horacio Gilabert<sup>g</sup>,   Miguel Castillo<sup>f</sup>, Jorge Saavedra<sup>i</sup>, Fulgencio Lisón<sup>k</sup>, Jordi Garcia-Gonzalo<sup>j</sup> and   Andrés Weintraub<sup>b,c</sup>

<sup>a</sup> Universidad Tecnológica Metropolitana, Departamento de Industria, Santiago, Chile  
<sup>b</sup> University of Chile, Industrial Engineering Department, Santiago, Chile  
<sup>c</sup> Complex Engineering System Institute - ISCI, Santiago, Chile  
<sup>d</sup> Department of Industrial Engineering, Faculty of Engineering, Universidad de Talca, Sede Curicó, Chile  
<sup>e</sup> Programa Doctorado en Ingeniería, Facultad de Ingeniería, Universidad de Talca, Sede Curicó, Chile  
<sup>f</sup> Forest Fire Laboratory, University of Chile, Box 9206, Santiago, Chile  
<sup>g</sup> Centro de Cambio Global, Pontificia Universidad Católica de Chile, Santiago, Chile  
<sup>h</sup> University of Chile, Department of Geophysics, Santiago, Chile  
<sup>i</sup> Forest Fire Analysis and Prediction Section, Corporación Nacional Forestal, Santiago, Chile  
<sup>j</sup> Forest Science and Technology Centre of Catalonia, Solsona, Spain  
<sup>k</sup> Ecosistemas Mediterráneos (ECOMED), Departamento de Ecología e Hidrología, Facultad de Biología, Universidad de Murcia, Campus de Espinardo, 30100, Murcia, Spain  

<sup>*</sup> Corresponding author.

# Disclaimer
This software is for research use only. There is no warranty of any kind; there is not even the implied warranty of fitness for use.



# Introduction
Spatial simulation of wildfires is a valuable tool for fire management, supporting both prevention and operational decision-making. However, many existing tools are not publicly available or require restrictive licenses. This paper introduces C2FK, an open-source simulator designed to model fire growth across Chilean landscapes and generate burn probability maps through iterative, spatially explicit simulations. Built on the Cell2Fire engine, C2FK integrates an adaptation of KITRAL, Chile’s national fire behavior system. The implementation includes new equations to estimate rate of spread and length-to-breadth ratio as functions of wind speed, using an elliptical fire growth model. It also incorporates a crown fire behavior module, extending predictive capacity beyond surface fires. We evaluate C2FK by comparing its outputs against synthetic and real wildfire scenarios, demonstrating accuracy and scalability. Cross-platform and parallel-computing enabled, C2FK provides a flexible, high-performance solution to support risk assessment, scenario analysis, and wildfire planning in Chile and other fire-prone environments.

**Please cite as:** [Carrasco-Barra, J., González-Olabarria, J. R., Matus-Olivares, C., Ulloa-Fierro, F., Soto, F., Palacios, D., Mahaluf, R., de la Barra, F., Espinoza, C., Vilches, M., Rivas, M., Badilla, F., Gilabert, H., Castillo, M., Saavedra, J., Lisón, F., Garcia-Gonzalo, J., & Weintraub, A. (2026). New extensions of Cell2Fire software for fire risk analysis and evaluation in Chilean forests. Environmental Modelling & Software.](https://doi.org/10.1016/j.envsoft.2026.107009)

# Usage guide
### Compiling
```bash
# dependencies
sudo apt install g++-12 libboost-all-dev libtiff-dev
# or brew
brew install gcc@12 libomp boost libtiff # llvm ?

# fork & clone 
git clone git@github.com:<YOU>/C2FK.git
cd C2FK/Cell2Fire

# compile
make 
# there area other makefiles for other platforms, e.g. makefile.macos
```
Other platform details at .github/workflows/build-*.yml and makefile.*
### Running simulations
```bash
Cell2Fire --input-instance-folder /path/to/input-data --output-folder /path/to/output-results --nsims 100
```
The basic information the simulator needs is fuel and weather data. These must be located in the input instance folder, and should be named "fuels.asc" or "fuels.tif" and "Weathers.csv" respectively. Additional information such as terrain elevation, canopy bulk density, and canopy base height can also be provided. Please use the examples found under `/data` to guide your input file names.
 ### Configuring simulations
There are many command line options available to configure the simulation.
| Argument              | Type   | Function                                                                                              |
| --------------------- | ------ | ----------------------------------------------------------------------------------------------------- |
| nsims                 | int    | Number of simulations to run.                                                                         |
| cros                  | bool   | True if crown fire should be included.                                                                |
| fmc                   | int    | Used in Kitral to calculate critical intensity. Default is 100.                                       |
| nthreads              | int    | Defines the number of threads to use for simulations. Default is 1.                                   |
| seed                  | int    | Seed for the random generator.                                                                        |
| IgnitionRad           | int    | If greater than 0, picks a point on the circumference of radius = IgnitionRadius from ignition point. |
| nweathers             | int    | Number of weather files. Used to randomly select one.                                                 |
| CCFFactor             | float  | Weighs by the cell’s CCF when calculating crown ROS in S&B. Default is 0.                             |
| EFactor               | float  | Weighs radial distance from the ellipse center. Default is 1.0.                                       |
| BFactor               | float  | Weighs back ROS and ellipse "c". Default is 1.0.                                                      |
| FFactor               | float  | Weighs flank ROS. Default is 1.0.                                                                     |
| HFactor               | float  | Weighs head ROS. Default is 1.0.                                                                      |
| ROS-Threshold         | float  | ROS threshold for fire to spread. Default is 0.1.                                                     |
| ROS-CV                | float  | Used to calculate a random ROSRV value. Default is 0.                                                 |
| FirebreakCells        | string | Firebreak plan, sets cells as “NonBurnable”.                                                          |
| weather               | string | Options: “rows”, “constants”, “distribution”, “random”. Default is “rows”.                            |
| output-folder         | string | Directory where results will be saved.                                                                |
| input-instance-folder | string | Directory containing all required files.                                                              |
| bbo                   | bool   | True to use Black Box Optimization.                                                                   |
| final-grid            | bool   | Saves grid state at the end of the simulation.                                                        |
| grids                 | bool   | Saves forest grids during the simulation.                                                             |
| ignitions             | bool   | Reads ignition points from file or uses random ones.                                                  |
| ignitionsLog          | bool   | Saves a log of attempted ignitions.                                                                   |
| verbose               | bool   | Prints ultra-detailed log.                                                                            |
| out-cfb               | bool   | Saves crown burned fraction. Only with `--cros`.                                                      |
| out-crown             | bool   | Saves layer with crown fire cells.                                                                    |
| out-ros               | bool   | Saves ROS per cell.                                                                                   |
| out-intensity         | bool   | Saves Byram fire intensities.                                                                         |
| out-fl                | bool   | Saves flame length results. In S&B, saves surface, crown, and max.                                    |
| output-messages       | bool   | Saves file with messages (origin, destination, time, ROS).                                            |


# Output examples
Most outputs are ASCII raster layers, of the same shape as the original fuels raster.

The following is the fireline intensity output for a small simulation. The cells that have 0 are cells that did not catch fire.
```bash
ncols 7
nrows 7
xllcorner 457900
yllcorner 5.7168e+06
cellsize 100
NODATA_value -9999
0 4389.03 0 0 0 0 0
0 0 17663.2 18731.9 0 4201.66 0
1711.45 0 1731.95 0 5487.64 9923.44 0
0 14655.2 6652.72 5804.41 4371.23 9348.01 0
0 9441.69 7127.24 0 0 0 0
0 0 7692.64 4389.03 3107.24 2032.65 0
0 8251.82 0 0 17663.2 18731.9 0
```

# Illustrative examples

## Simulated fire propagation scars and isochrones for: (A) Talcamávida, (B) Santa Elcira, and (C) Trupán II.  
The red point indicates the ignition location. The first columns highlight the initial stages of fire spread from the ignition point, while the final column shows the complete temporal evolution of the fire. This layout enables visualization of both early-stage spread dynamics and overall fire extent.
![Comparison of Real wildfire events](Output/propagation_scars.jpeg)

# About us

We are a research group that seeks solutions to complex problems arising from the terrestrial ecosystem and its natural and anthropogenic disturbances, such as wildfires.

Currently hosted at [ISCI](https://isci.cl/) offices.

Contact us on [Discord](https://discord.gg/A5jwWJKT).

Visit our [public webpage](http://www.fire2a.com/).
