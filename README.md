# Ascending_neuron_screen_analysis_pipeline
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)

This repository is for generating the figures published in the paper-- [**Ascending neurons convey high-level behavioral-state signals to multimodal sensory and action selection centers in the Drosophila brain**]().

This pipeline is made and run in Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-76-generic x86_64). 
 
## Content
- [Installation](#installation)
- [Download the preprocessed experimental data](#Download-the-preprocessed-experimental-data)
- [Reproducing the figures](#reproducing-the-figures)
 

## Installation
**1. Install the python environment** ```AN``` ** to be able to run ```.py``` scripts as guided below:**
- Change directory to your ```/Ascending_neuron_screen_analysis_pipeline``` where ```AN_env_public.yml``` locates by:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline
```
- Install the python environment with specified package in AN_env_public.yml
```bash
$ conda env create -f AN_env_public.yml
```
 


**2. Install DeepLabCut of CPU version used in this paper in its own environment (make sure leave** ```AN``` **environment by** ```conda deactivate``` **before the following steps)**
- Downlaod and install DeepLabCut:
```bash
$ git clone git+https://github.com/DeepLabCut/DeepLabCut.git@413ae5e2c410fb9da3da26c333b6a9b87ab6c38f#egg=deeplabcut
```
- Change direcotry to ```/conda-environments``` where the ```DLC-CPU.yaml``` locates:
```bash
$ cd ../../DeepLabCut/conda-environments
```
- Create DLC-CPU environment and install CPU version of DeepLabCut:
```bash
$ conda env create -f DLC-CPU.yaml
```

**3. Install R and the packages**
We use R 3.6.1 to develop some part of anaylsis pipeline, you can find more information about R [here](https://stat.ethz.ch/pipermail/r-announce/2019/000643.html).

- Install R version 3.6.1 (2019-07-05) and the r-base-dev package to be able to compile R packages:
```bash
$ sudo apt-get update 
$ sudo apt-get install r-base-dev=3.6.1
```

- Launch R to install packages by entering ```R``` in the terminal for installing the following packages:
```bash
$ R
```
- Install R packages used in this paper in R:
```R
> install.packages("ggpmisc")
> install.packages("ggplot2")
> install.packages("tidyverse")
> install.packages("tidyr")
> install.packages("dplyr")
> install.packages("reshape2")
```

**Optional**
Now, the dependencies of ```AN``` environment, DeepLabCut, and R are installed.
If you need to use AN independently anytime to check python script seperately, remeber activate ```AN``` environment manually before running the script by:
```bash
$ source activate AN
$ python name.py
```

If you need to use DeepLabCut independently anytime, remember activate the environment manually before running the script by:
```bash
$ source activate DLC-CPU
$ python name.py
```

If ```source``` doesn't work, try using ```conda``` instead.

There is no environment for ```R```. 
To run the R script in the terminal independently:
```bash
$ Rscript name.R
```



## Download the preprocessed experimental data
Download the content from [Harvard dataverse]() and make sure the location of data content inside each numbered folder are as below:

```bash
Ascending_Project_public
├── 00_behavior_data_preprocess
│   ├── CO2puff_regressors
│   ├── df3dResults_ballRot_captureMeta
│   └── PE_regressors
├── 01_behavior_annotation_for_behavior_classifier
│   └── behaviour_annotations.csv
├── 03_general_2P_exp
│   ├── MAN
│   ├── R15E08
│   ├── R30A08
.   .   ...
.   .   ...
.   .   ...
│   ├── SS52147
├── 04_mcfo_traced_singleAN_exp
│   ├── MCFO
│   ├── VFB
│   └── VNC
├── 05_offBall_onBall_2P_exp
│   ├── SS38631
│   └── SS51017
├── 06_SS36112-air_vs_co2_puff
│   └── SS36112
├── 07_SS31232-PE_exp
│   └── SS31232
├── DLC_model_for_labelling_proboscis
│   ├── config.yaml
│   ├── dlc-models
│   ├── evaluation-results
│   ├── labeled-data
│   ├── training-datasets
│   └── videos
```
 
## Reproducing the figures

**Note:** before running the following scripts, make sure python environment and R packages are all installed (see the installation guide)
In the folder ```/scripts_for_public```, you can generate the plots of figures by following the order depecited in the diagram to start the analysis from preprocessed data to the plots presented in the indicated figure panels. The details are shown below:

**Content**
- [FigS1](#Figures-from-dataset-00_)
- [Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a](#Figures-from-dataset-00_-01_-and-03_)
- [Fig7a](#Figures-from-dataset-00_-01_-and-03_)
- [Fig10b_right, Fig10c](#Figures-from-dataset-00_-01_-and-03_)
- [FigS2](#Figures-from-dataset-03_)
- [FigS3](#Figures-from-dataset-03_)
- [Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b](#Figures-from-dataset-03_)
- [Fig6c, Fig7e](#Figures-from-dataset-03_)
- [FigS5](#Figures-from-dataset-03_)
- [Fig3, FigS4](#Figures-from-dataset-04_)
- [FigS7](#Figures-from-dataset-05_)
- [FigS6](#Figures-from-dataset-06_)
- [Fig10b_left](#Figures-from-dataset-07_)


### Figures from dataset 00_: 
- **FigS1**: Semi-automated detection of proboscis extensions.

### Figures from dataset 00_, 01_ and 03_: 
- **Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a**: Prediction of neural activity; Fig7c: Prediction of neural activity difference between left and right neurons from turning.
- **Fig7a**: Explained variance matrix by turning.
- **Fig10b_right, Fig10c**: Prediction of neural activity from convoluted PE.

### Figures from dataset 03_:
- **FigS2**: Joint angle and behavior covariance matrix.
- **FigS3**: Behavioral event-based average enural activity. 
- **Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b**: Behavioral event-based average enural activity. 
- **Fig6c, Fig7e**: Neural activity-based ball rotation.
- **FigS5**: ANs from SS36112 likely specifically respond to puff stimulation rather than backward walking.


### Figures from dataset 04_:
- **Fig3, FigS4**: Large-scale anatomical quantification of adult Drosophila ascending neuron projections to the brain and ventral nerve cord.

### Figures from dataset 05_:
- **FigS7**: ANs that are active off of the spherical treadmill.

### Figures from dataset 06_:
-  **FigS6**: ANs from SS36112 respond to both air and CO2 puff.

### Figures from dataset 07_:
- **Fig10b_left**: Summary of neural activity of each PE during PE train.













