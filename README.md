# Ascending_neuron_screen_analysis_pipeline
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)

This repository is for generating the figures published in the paper of [**Ascending neurons convey high-level behavioral-state signals to multimodal sensory and action selection centers in the Drosophila brain**]().
 
## Content
- [Installation](#installation)
- [Download the preprocessed experimental data](#Download-the-preprocessed-experimental-data)
- [Reproducing the figures](#reproducing-the-figures)
 

## Installation
**1. To be able to execute the codes and NeLy homemade packages, install the python environment** ```AN``` **as guided below:**
- Change directory to your ```/Ascending_neuron_screen_analysis_pipeline``` where ```AN_env_public.yml``` locates by:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline
```
- Install the python environment with specified package in AN_env_public.yml
```bash
$ conda env create -f AN_env_public.yml
```
 
**2. Install [NeLy](https://github.com/NeLy-EPFL)'s DeepFly3D and df3dPostProcess packages in** ```AN``` **environment as guided below:**

- Activate to the AN environemnt:
```bash
$ source activate AN
```
or if ```source``` doesn't work, try:
```bash
$ conda activate AN
```

- Dowload and install DeepFly3D:
```bash
$ pip install git+https://github.com/NeLy-EPFL/DeepFly3D.git@974f839e224a41e7c5774e2effddf8ff763da88a#egg=deepfly
```

- Dowload and install df3dPostProcess:
```bash
$ pip install git+https://github.com/NeLy-EPFL/df3dPostProcessing.git@b6be9b0587db55023bb41858c6b49d4e11a98e9f#egg=df3dPostProcessing
```

**3. Install CPU version of DeepLabCut used in this paper in its own environment (make sure leave** ```AN``` **environment by** ```conda deactivate``` **before the following steps)**
- Downlaod and install DeepLabCut:
```bash
git clone git+https://github.com/DeepLabCut/DeepLabCut.git@413ae5e2c410fb9da3da26c333b6a9b87ab6c38f#egg=deeplabcut
```
- Change direcotry to ```/conda-environments``` where the ```DLC-CPU.yaml``` locates:
```bash
cd ../../DeepLabCut/conda-environments
```
- Create DLC-CPU environment and install CPU version of DeepLabCut:
```bash
conda env create -f DLC-CPU.yaml
```

**4. Install R and the packages**
- Install R system:
```bash
sudo apt-get update 
sudo apt-get install r-base
```
- Install r-base-dev package to be able to compile R packages:
```bash
sudo apt-get install r-base-dev
```

- Launch R to install packages by entering ```R``` in the terminal for installing the following packages:
```bash
R
```
- Install R packages used in this paper in R:
```bash
install.packages("ggpmisc")
install.packages("ggplot2")
install.packages("tidyverse")
install.packages("tidyr")
install.packages("dplyr")
install.packages("reshape2")
```

**Optional**
Now, the dependencies of ```AN``` environment, DeepLabCut, and R are installed.
If you need to use DeepLabCut independently anytime, please activate the environment manually by:
```bash
source activate DLC-CPU
```

If you need to use AN independently anytime, activate ```AN``` environment manually by:
```bash
source activate AN
```



## Download the preprocessed experimental data
Download the data into the corresponding folders as structured here from [Harvard Dataverse]():

 
## Reproducing the figures

**Note:** before running the following scripts, make sure that the python environment and R package are all installed (see the installation guide)
In the folder ```/scripts_for_public```, you can generate the plots of figures by following the order of ```_xx.run``` scripts to start the analysis from preprocessed data to the plots presented in the indicated figure panels. The details are shown below:

- 













