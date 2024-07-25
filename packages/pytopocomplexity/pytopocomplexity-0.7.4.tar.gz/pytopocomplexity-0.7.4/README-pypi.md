# pyTopoComlexity (v0.7.4)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11239338.svg)](https://doi.org/10.5281/zenodo.11239338)

`pytopocomplexity` is an open-source Python package designed to measure the topographic complexity (i.e., surface roughness) of land surfaces using digital elevation model (DEM) data. This package includes modules for three methods commonly used in the fields of geomorphology and oceanography for measuring topographic complexity, which are not fully available in Geographic Information System (GIS) software like QGIS.

| Modules  | Method Descriptions |
| ------------- | ------------- |
| pycwtmexhat.py  | Quanitfy the wavelet-based curvature of the land surface using two-dimensional continuous wavelet transform (2D-CWT) with a Mexican Hat wevalet |
| pyfracd.py  | Conduct fractal dimension analysis on the land surface |
| pyrugostiy.py  | Calculate rugosity indext of the land surface |

## Installation

```
pip install pytopocomplexity
```

## Modules for Surface Complexity Measurement

### 1. `pycwtmexhat`: 2D Continuous Wavelet Transform Method

```python
from pytopocomplexity import pycwtmexhat
```

The module `pycwtmexhat` uses two-dimensional continuous wavelet transform (2D-CWT) with a Mexican Hat wevalet to measure the topographic complexity (i.e., surface roughness) of a land surface from a Digital Elevation Model (DEM). Such method quanitfy the wavelet-based curvature of the surface, which has been proposed to be a effective geomorphic metric for identifying and estimating the ages of historical deep-seated landslide deposits.

The method and early version of the code was developed by Dr. Adam M. Booth (Portland State Univeristy) in [2009](https://doi.org/10.1016/j.geomorph.2009.02.027), written in MATLAB (Source code available from [Booth's personal website](https://web.pdx.edu/~boothad/tools.html)). This MATLAB code was later revised and adapted by Dr. Sean R. LaHusen (Univeristy of Washington) and Dr. Erich N. Herzig (Univeristy of Washington) in their research ([LaHusen et al., 2020](https://doi.org/10.1126/sciadv.aba6790); [Herzig et al. (2023)](https://doi.org/10.1785/0120230079)). Dr. Larry Syu-Heng Lai (Univeristy of Washington), under the supervision of Dr. Alison R. Duvall (Univeristy of Washington), translated the code into this optimized open-source Python version in 2024.

### 2. `pyfracd`: Fractal Dimentsion Analysis

```python
from pytopocomplexity import pyfracd
```

The `pyfracd` module calculates local fractal dimensions to assess topographic complexity. It also computes reliability parameters such as the standard error and the coefficient of determination (R²). The development of pyfracd is made possible through the gratitude of Dr. Eulogio Pardo-Iguzquiza, who kindly shared his Fortran code used in his recent publication [Pardo-Igúzquiza and Dowd (2022)](https://doi.org/10.1016/j.icarus.2022.115109).

The local fractal dimension is determined by intersecting the surface within a moving window with four vertical planes in principal geographical directions, simplifying the problem to one-dimensional topographic profiles. The fractal dimension of these profiles is estimated using the variogram method, which models the relationship between dissimilarity and distance using a power-law function. While the fractal dimension value does not directly scale with the degree of surface roughness, smoother or more regular surfaces generally have lower fractal dimension values (closer to 2), whereas surfaces with higher fractal dimension values tend to be more complex or irregular. This method has been applied in terrain analysis for understanding spatial variability in surface roughness, classifying geomorphologic features, uncovering hidden spatial structures, and supporting geomorphological and geological mapping on Earth and other planetary bodies.

### 3. `pyrugosity`: Rugosity Index

```python
from pytopocomplexity import pyrugosity
```

The module `pyrugosity` measure rugosity index of the land surface, which is widely used to assess landscape structural complexity. The development of this module is influenced by another open-source tool [`Rugosity_Calculator`](https://github.com/drk944/Rugosity_Calculator) created by [drk944](https://github.com/drk944).

The rugosity index is determined as the ratio of the real surface area to the geometric surface area, highlighting smaller-scale variations in surface height. This module adapt triangulated irregular networks method ([Jenness, 2004](https://doi.org/10.2193/0091-7648(2004)032[0829:CLSAFD]2.0.CO;2)), which approximate the surface area of with within each 9 cell as the sum of 8 truncated-triangle area connecting each cell centerpoint with the centerpoints of the 8 surrounding cells. The geometric surface area is assumed to be the planimetric area of the center cell. By definition, the rugosity index is as a minimum value of one (completely flate surface). Typical valuesrange from one to three although larger values are possible in very steep terrains. Such method has been applied in classifying seafloor types by marine geologists and geomorphologist, small-scale hydrodynamics by oceanographers, and studying available habitats in the landscape by ecologists and coral biologists.

## Requirements
For `pytopocomplexity` package
* Python >= 3.10
* `numpy`
* `scipy`
* `rasterio`
* `dask`
* `matplotlib`
* `tqdm`
* `numba`

## License
pyTopoComlexity is licensed under the [Apache License 2.0](LICENSE).
