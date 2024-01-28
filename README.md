# An Analysis of Wind Speed and Power Density in the North Sea

> In the face of climate change and global warming, the issue of turning the
> energy production CO2 neutral and sustainable is evermore pressing. Thus, wind
> energy harnessed by offshore wind turbine parks plays a crucial role in
> achieving this goal. This paper explores methods for asserting the viability of
> wind turbines by modelling the distribution of wind speeds as Weibull
> distributions, computing the expected surface power density and applying a
> Gaussian Process time-series regression for interpolation and prediction.  based
> on wind speed measurements conducted on the island of Helgoland in the
> North-Sea.

This work was done as part of Data Literacy course at University of Tübingen.
This is the repository containing all the relevant figures, source and tex
files.

## Content

1. `citation_sources`: A directory contains the paper's sources in PDF format.
2. `notes`: A directory contains multiple jupyter notebooks used in the analysis.
This is where all figures are created.
3. `paper`: A directory contains the LaTeX files needed to generate the paper in
PDF format. Also, all figures are saved in paper/fig
4. `util`: A directory contains python scripts used in the analysis.
5. `Makefile`: Used for conviently creating a conda environment with all needed
dependencies, compiling the tex file to a pdf, deleting the data folder and
other tasks. See below for a more in-depth description.

## Installation

Use the accompanied Makefile to manage the conda enviroment, clean the
downloaded data and create the paper's PDF.

#### Activate the conda enviroment and install all dependencies

```bash
make load-env
```

#### Delete the downloaded data

```bash
make clean
```

#### Create the article pdf

```bash
make pdf
```

#### Delete the article pdf

```bash
make clean-pdf
```
