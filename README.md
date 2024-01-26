# Data Literacy Project 

Project title: **'An Analysis of Wind Speed and Power Density in the North Sea'** 

This work was done as part of Data Literacy course at Universität Tübingen 

## Content
1. citation_sources: A directory contains the paper's sources in PDF format. 
2. notes: A directory contains multiple jupyter notebooks used in the analysis. 
3. paper: A directory contains the LaTeX files needed to generate the paper in PDF format.  
4. util: A directory contains python scripts used in the analysis.
5. Makefile: Bash script to manage the conda enviroment, storing the data and creating the paper's PDF.

## Installation
Use the accompanied makefile to manage the conda enviroment, clean the downloaded data and create the paper's PDF. 

#### Activate the conda enviroment
```bash
make load-env
```

#### Delete the downloaded data
```bash
make clean
```

#### Create the article pdf
```bash
make clean
```

#### Delete the article pdf
```bash
make clean-pdf
```

## Contribution

## License

[MIT](https://choosealicense.com/licenses/mit/)
