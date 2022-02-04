# Ascending_neuron_screen_analysis_pipeline
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)

This repository is for generating the figures published in the paper-- [**Ascending neurons convey high-level behavioral-state signals to multimodal sensory and action selection centers in the Drosophila brain**]().

This pipeline is made and run in Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-76-generic x86_64). 
 
## Content
- [Installation](#installation)
- [Download preprocessed experimental data](#Download-preprocessed-experimental-data)
- [Reproducing the figures](#reproducing-the-figures)
 

## Installation
### 1. Install the python environment ```AN``` to be able to run ```.py``` scripts as guided below:
- Change directory to your ```../Ascending_neuron_screen_analysis_pipeline``` folder where ```AN_env_public.yml``` locates:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline
```
- Install the python environment with specified package in AN_env_public.yml
```bash
$ conda env create -f AN_env_public.yml
```
 


### 2. Install DeepLabCut of CPU version used in this paper in its own environment (make sure leave ```AN``` environment by ```conda deactivate``` before the following steps)
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
And DeepLabcut is intalled and ready to use.


### 3. Install R and the packages
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
│   └── SS52147
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
- [Figures from dataset 00_](#figures-from-dataset-00_):
  - [FigS1: Semi-automated detection of proboscis extensions](#figS1:-Semi-automated-detection-of-proboscis-extensions)

- [Figures from dataset 00_, 01_ and 03_](#figures-from-dataset-00_,-01_-and-03_):
  - [Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a: Prediction of neural activity](#Fig4a,-Fig5a,-Fig6a,-Fig7b,-Fig8a,-Fig9a,-Fig10a:-Prediction-of-neural activity)
  - [Fig7c](#Fig7c)
  - [Fig10b_right, Fig10c](#Fig10b_right,-Fig10c)
  - [FigS10](#FigS10)
  - [Fig2, FigS4 top](#Fig2,-FigS4-top)
  - [Fig7a](#Fig7a)

- [Figures-from-dataset-03_](#Figures-from-dataset-03_):
  - [FigS2](#FigS2)
  - [FigS3](#FigS3)
  - [Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b](#Fig4b,-Fig5b,-Fig6b,-Fig7b,-Fig8b,-Fig9b)
  - [Fig6c, Fig7e](#Fig6c,-Fig7e)
  - [FigS5](#FigS5)

- [Figures-from-dataset-04_](#Figures-from-dataset-04_):
  - [Fig3, FigS4](#Figures-from-dataset-04_)

- [Figures-from-dataset-05_](#Figures-from-dataset-05_):
  - [FigS7](#Figures-from-dataset-05_)

- [Figures-from-dataset-06_](#Figures-from-dataset-06_):
  - [FigS6](#Figures-from-dataset-06_)

- [Figures-from-dataset-07_](#Figures-from-dataset-07_):
  - [Fig10b_left](#Figures-from-dataset-07_)





### Figures from dataset 00_: 
#### FigS1: Semi-automated detection of proboscis extensions
```bash
$ Ascending_Project_public/scripts_for_public/._00-0-plot_FigS1-exemplar_DLC_proboscisLabel_PEevt_detection.run
```
The results can be found in ```Ascending_Project_public/output/FigS1-exemplar_PEevt_detection/```

### Figures from dataset 00_, 01_ and 03_: 
Intermediate file have to be generated first:
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-1_train_behavior_classifier.run
$ Ascending_Project_public/scripts_for_public/._00_01_03-2_predict_behavior_and_sync_beh_w_DFF.run
```
Once the intermediate results are generated, following plots can be made by corredponding bash scripts:
#### Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a: Prediction of neural activity
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-2-plot_Fig4a_5a_6a_7b_8a_9a_10a-Plot_prediction_rawDFF_traces.run
```
#### Fig7c: Prediction of neural activity difference between left and right neurons from turning
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-2-plot_Fig7c-Plot_dDFF_traces_fit_turning.run
```
#### Fig10b_right, Fig10c: Prediction of neural activity from convoluted PE
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-2-plot_Fig10b_right_10c-Plot_convPE.run
```
#### FigS10: Behavior classifier confusion matrix
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-2-plot_FigS10-beh_jangle_confusionMat.run
```


#### Fig2, FigS4 top: GLM of joint angle, leg, leg pair, behavior in predicitng neural activity
For visulazing GLM matrix, further intermediate GLM results have to be generated first for make the plot:
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-3_glm_of_beh_leg_legPair_jangle_DFF.run
```
Then, plot with:
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-3-plot_Fig2abcd_S4-Plot_glmmat_of_beh_leg_legPair_jangle_DFF.run
```


#### Fig7a: Explained variance matrix of turning in predicitng neural activity
For visulazing turning r-squared matrix, further intermediate results have to be generated first for make the plot:
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-4_turn_mat_analysis.run
```
Then, plot with:
```bash
$ Ascending_Project_public/scripts_for_public/._00_01_03-4-plot_Fig7a-Plot_turn_analysis_matrix.run
```


### Figures from dataset 03_:
#### FigS2: Joint angle and behavior covariance matrix
```bash
$ Ascending_Project_public/scripts_for_public/._03-0-plot_FigS2-jangle_beh_covariance.run
```

#### FigS3: Behavioral event-based average enural activity
Intermediate results of averaging neural activity of each behavioral epoch need to be generated beforehand:
```bash
$ Ascending_Project_public/scripts_for_public/._03-1_prep_DFF_beh_mat.run
```
Then, the results can be visualized with following scripts:
```bash
$ Ascending_Project_public/scripts_for_public/._03-2-plot_FigS3-Plot_DFFmat.run
```

#### Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b: Behavioral event-based average enural activity
```bash
$ Ascending_Project_public/scripts_for_public/._03-2-plot_Fig4b_5b_6b_7d_8b_9b-Plot_BehEvt_avgDFF.run
```

#### Fig6c, Fig7e: Neural activity-based ball rotation
Intermediate results of neural event detection need to be generated beforehand:
```bash
$ Ascending_Project_public/scripts_for_public/._03-3_prep_DFFevt_analysis.run
```
Then, the results can be visualized with following scripts:
```bash
$ Ascending_Project_public/scripts_for_public/._03-3-plot_Fig6c_7e-Plot_DFFevt_analysis.run
```

#### FigS5: ANs from SS36112 likely specifically respond to puff stimulation rather than backward walking
Intermediate results of puff and backward walking event detection need to be generated beforehand:
```bash
$ Ascending_Project_public/scripts_for_public/._03-4_prep_SS36112_independentBW_vs_CO2puffBW_analysis.run
```
Then, the results can be visualized with following scripts:
```bash
$ Ascending_Project_public/scripts_for_public/._03-4-plot-FigS5-SS36112_independentBW_vs_CO2puffBW_analysis.run
```


### Figures from dataset 04_:
#### Fig3, FigS4: Large-scale anatomical quantification of adult Drosophila ascending neuron projections to the brain and ventral nerve cord

Intermediate results of puff and backward walking event detection need to be generated beforehand:
```bash
$ Ascending_Project_public/scripts_for_public/._04-1_prep_singleAN_innervation_mat.run
```
Then, the results can be visualized with following scripts:
```bash
$ Ascending_Project_public/scripts_for_public/._04-1-plot_Fig3_S4-Plot_singleAN_innervation_mat.run
```

### Figures from dataset 05_:
#### FigS7: ANs that are active off of the spherical treadmill
```bash
$ Ascending_Project_public/scripts_for_public/._05-0-plot_FigS7-offBall_onBall_comparison.run
```
### Figures from dataset 06_:
####  FigS6: ANs from SS36112 respond to both air and CO2 puff
```bash
$ Ascending_Project_public/scripts_for_public/._06-0-plot_FigS6-Plot_air_vs_CO2puff.run
```

### Figures from dataset 07_:
#### Fig10b_left: Summary of neural activity of each PE during PE train
```bash
$ Ascending_Project_public/scripts_for_public/._07-0-plot_Fig10b_left-DFF_per_PE.run
```












