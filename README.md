# An Analysis of Wind Energy Potential in the North Sea

> In the face of climate change, it is widely agreed
> that the energy production has to rely on more
> sustainable and renewable forms of harnessing
> energy. Offshore wind turbine parks play a crucial
> role in increasing the share of green energy. This
> paper explores probabilistic methods of assessing
> the wind energy potential and potential trends in
> data collected on Helgoland by considering wind
> speeds as a Weibull distributed random variable.
> Further, for forecasting, the monthly expected
> wind power density is extrapolated by a Gaussian
> process regression model.

This work was done as part of Data Literacy course at University of Tübingen.
This is the repository containing all the relevant figures, source and tex
files.

## Content

1. `notes`: A directory contains multiple jupyter notebooks used in the analysis.
This is where all figures are created.
2. `paper`: A directory contains the LaTeX files needed to generate the paper in
PDF format. Also, all figures are saved in paper/fig
3. `util`: A directory contains python scripts used in the analysis.
4. `Makefile`: Used for conviently creating a conda environment with all needed
dependencies, compiling the tex file to a pdf, deleting the data folder and
other tasks. See below for a more in-depth description.

## Installation & Usage

First, setup the a new Python environment using conda. Simply run `make env` to
setup a new enivornment called `datalit`. Then, run the notesbook in `notes/` to
produce all plots needed for the paper. Finally, use `make pdf` to produce the
paper's PDF. See below for other `make` commands:

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
