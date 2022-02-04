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
To be able to run all the script, python and R have to be installed.

To be able to intall the environment with specific version of python packages, please install Anaconda first if you don't have. 

Install Anaconda --> https://www.anaconda.com/
### 1. Install python environment ```AN``` to be able to run ```.py``` scripts by following the guidance below:
Clone repository:
```bash 
$ cd ../to/where/you/want/
$ git clone https://github.com/NeLy-EPFL/Ascending_neuron_screen_analysis_pipeline.git
```
Change directory to your ```../Ascending_neuron_screen_analysis_pipeline``` folder where ```AN_env_public.yml``` locates:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline
```
Install ```AN``` python environment with packages in ```AN_env_public.yml```:
```bash
$ conda env create -f AN_env_public.yml
```
 


### 2. Install DeepLabCut of CPU version used in this paper in its own environment (make sure leave ```AN``` environment by ```conda deactivate``` before the following steps)
Downlaod and install DeepLabCut:
```bash
$ git clone git+https://github.com/DeepLabCut/DeepLabCut.git@413ae5e2c410fb9da3da26c333b6a9b87ab6c38f#egg=deeplabcut
```
Change direcotry to ```/conda-environments``` where the ```DLC-CPU.yaml``` locates:
```bash
$ cd ../../DeepLabCut/conda-environments
```
Create DLC-CPU environment and install CPU version of DeepLabCut:
```bash
$ conda env create -f DLC-CPU.yaml
```
And DeepLabcut is intalled and ready to use.


### 3. Install R and the packages
We use R 3.6.1 to develop some part of anaylsis pipeline, you can find more information about R [here](https://stat.ethz.ch/pipermail/r-announce/2019/000643.html).

Install R version 3.6.1 (2019-07-05) and the r-base-dev package to be able to compile R packages:
```bash
$ sudo apt-get update 
$ sudo apt-get install r-base-dev=3.6.1
```

Launch R to install packages by entering ```R``` in the terminal for installing the following packages:
```bash
$ R
```
Install R packages used in this paper in R:
```R
> install.packages("ggpmisc")
> install.packages("ggplot2")
> install.packages("tidyverse")
> install.packages("tidyr")
> install.packages("dplyr")
> install.packages("reshape2")
```

**Optional**

Now, ```AN``` conda environment, DeepLabCut, and R are installed.
If you want to to check python script seperately, remeber activate ```AN``` environment manually before running the each ```.py``` script by:
```bash
$ source activate AN
$ python name.py
```

If you want to use DeepLabCut independently anytime, remember to activate DLC-CPU environment manually before running the script by:
```bash
$ source activate DLC-CPU
$ python name.py
```
In our case, only 



If ```source``` doesn't work, try using ```conda``` instead.

There is no environment for ```R```. 
To run the R script in the terminal independently:
```bash
$ Rscript name.R
```



## Download the preprocessed experimental data
Download the content from [Harvard dataverse](https://dataverse.harvard.edu/dataverse/AN) and make sure the location of data content inside each numbered folder are as below:

```bash
Ascending_neuron_screen_analysis_pipeline
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
To start running the analysis pipeline, execute the following ```.run``` script from the folder ```Ascending_Project_public/scripts_for_public/``` by:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline/scripts_for_public/
```
Execute the script by typeing ```./``` before the script fileame, for example:
```bash
$ ./_00-0-plot_FigS1-exemplar_DLC_proboscisLabel_PEevt_detection.run
```
The intermediate results have to be generated in the order as guided below to be able to generate the plots. Please check the diagram in each session which depicts the workflow from specified dataset to the ouput plots. 

### Content
- [Figures from dataset 00_](#00):
  - [FigS1: Semi-automated detection of proboscis extensions](#FigS1)

- [Figures from dataset 00_, 01_ and 03_](#00-01-03):
  - [Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a: Prediction of neural activity](#Fig4a-Fig5a-Fig6a-Fig7b-Fig8a-Fig9a-Fig10a)
  - [Fig7c: Prediction of neural activity difference between left and right neurons from turning](#Fig7c)
  - [Fig10b_right, Fig10c: Prediction of neural activity from convoluted PE](#Fig10b_right-Fig10c)
  - [FigS10: Behavior classifier confusion matrix](#FigS10)
  - [Fig2, FigS4 top: GLM of joint angle, leg, leg pair, behavior in predicitng neural activity](#Fig2-FigS4-top)
  - [Fig7a: Explained variance matrix of turning in predicitng neural activity](#Fig7a)

- [Figures-from-dataset-03_](#03):
  - [FigS2: Joint angle and behavior covariance matrix](#figS2)
  - [FigS3: Behavioral event-based average enural activity](#FigS3)
  - [Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b: Behavioral event-based average enural activity](#Fig4b-Fig5b-Fig6b-Fig7b-Fig8b-Fig9b)
  - [Fig6c, Fig7e: Neural activity-corresponding ball rotation](#Fig6c-Fig7e)
  - [FigS5: ANs from SS36112 likely specifically respond to puff stimulation rather than backward walking](#FigS5)

- [Figures-from-dataset-04_](#04):
  - [Fig3, FigS4: Large-scale anatomical quantification of adult Drosophila ascending neuron projections to the brain and ventral nerve cord](#Fig3-FigS4)

- [Figures-from-dataset-05_](#05):
  - [FigS7: ANs that are active off of the spherical treadmill](#FigS7)

- [Figures-from-dataset-06_](#06):
  - [FigS6: ANs from SS36112 respond to both air and CO2 puff](#FigS6)

- [Figures-from-dataset-07_](#07):
  - [Fig10b_left: Summary of neural activity of each PE during PE train](#Fig10b_left)





### Figures from dataset 00_: <span id="00"><span>
 
<p align="center">
  <img align="left" width="200" src="/images/Code_overflow_git_w_data_00.png">
</p>
 
#### FigS1: Semi-automated detection of proboscis extensions <span id="FigS1"><span>
```bash
$ ./_00-0-plot_FigS1-exemplar_DLC_proboscisLabel_PEevt_detection.run
```
The results can be found in ```Ascending_Project_public/output/FigS1-exemplar_PEevt_detection/```

### Figures from dataset 00_, 01_ and 03_: <span id="00-01-03"><span>

<p align="center">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_00_01_03.png">
</p>

Intermediate file have to be generated first:
```bash
$ ./_00_01_03-1_train_behavior_classifier.run
$ ./_00_01_03-2_predict_behavior_and_sync_beh_w_DFF.run
```
Once the intermediate results are generated, following plots can be made by corredponding bash scripts:
#### Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a: Prediction of neural activity <span id="Fig4a-Fig5a-Fig6a-Fig7b-Fig8a-Fig9a-Fig10a"><span>
```bash
$ ./_00_01_03-2-plot_Fig4a_5a_6a_7b_8a_9a_10a-Plot_prediction_rawDFF_traces.run
```
#### Fig7c: Prediction of neural activity difference between left and right neurons from turning <span id="Fig7c"><span>
```bash
$ ./_00_01_03-2-plot_Fig7c-Plot_dDFF_traces_fit_turning.run
```
#### Fig10b_right, Fig10c: Prediction of neural activity from convoluted PE <span id="Fig10b_right-Fig10c"><span>
```bash
$ ./_00_01_03-2-plot_Fig10b_right_10c-Plot_convPE.run
```
#### FigS10: Behavior classifier confusion matrix <span id="FigS10"><span>
```bash
$ ./_00_01_03-2-plot_FigS10-beh_jangle_confusionMat.run
```


#### Fig2, FigS4 top: GLM of joint angle, leg, leg pair, behavior in predicitng neural activity <span id="Fig2-FigS4-top"><span>
For visulazing GLM matrix, further intermediate GLM results have to be generated first for make the plot:
```bash
$ ./_00_01_03-3_glm_of_beh_leg_legPair_jangle_DFF.run
```
Then, plot with:
```bash
$ ./_00_01_03-3-plot_Fig2abcd_S4-Plot_glmmat_of_beh_leg_legPair_jangle_DFF.run
```


#### Fig7a: Explained variance matrix of turning in predicitng neural activity <span id="Fig7a"><span>
For visulazing turning r-squared matrix, further intermediate results have to be generated first for make the plot:
```bash
$ ./_00_01_03-4_turn_mat_analysis.run
```
Then, plot with:
```bash
$ ./_00_01_03-4-plot_Fig7a-Plot_turn_analysis_matrix.run
```


### Figures from dataset 03_: <span id="03"><span>

<p align="center">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_03.png">
</p>

#### FigS2: Joint angle and behavior covariance matrix <span id="FigS2"><span>
```bash
$ ./_03-0-plot_FigS2-jangle_beh_covariance.run
```

#### FigS3: Behavioral event-based average enural activity <span id="FigS3"><span>
Intermediate results of averaging neural activity of each behavioral epoch need to be generated beforehand:
```bash
$ ./_03-1_prep_DFF_beh_mat.run
```
Then, the results can be visualized with following scripts:
```bash
$ ./_03-2-plot_FigS3-Plot_DFFmat.run
```

#### Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b: Behavioral event-based average enural activity <span id="Fig4b-Fig5b-Fig6b-Fig7b-Fig8b-Fig9b"><span>
```bash
$ ./_03-2-plot_Fig4b_5b_6b_7d_8b_9b-Plot_BehEvt_avgDFF.run
```

#### Fig6c, Fig7e: Neural activity-corresponding ball rotation <span id="Fig6c-Fig7e"><span>
Intermediate results of neural event detection need to be generated beforehand:
```bash
$ ./_03-3_prep_DFFevt_analysis.run
```
Then, the results can be visualized with following scripts:
```bash
$ ./_03-3-plot_Fig6c_7e-Plot_DFFevt_analysis.run
```

#### FigS5: ANs from SS36112 likely specifically respond to puff stimulation rather than backward walking <span id="FigS5"><span>
Intermediate results of puff and backward walking event detection need to be generated beforehand:
```bash
$ ./_03-4_prep_SS36112_independentBW_vs_CO2puffBW_analysis.run
```
Then, the results can be visualized with following scripts:
```bash
$ ./_03-4-plot-FigS5-SS36112_independentBW_vs_CO2puffBW_analysis.run
```


### Figures from dataset 04_: <span id="04"><span>

<p align="center">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_04.png">
</p>

#### Fig3, FigS4: Large-scale anatomical quantification of adult Drosophila ascending neuron projections to the brain and ventral nerve cord <span id="Fig3_ FigS4"><span>

Intermediate results of puff and backward walking event detection need to be generated beforehand:
```bash
$ ./_04-1_prep_singleAN_innervation_mat.run
```
Then, the results can be visualized with following scripts:
```bash
$ ./_04-1-plot_Fig3_S4-Plot_singleAN_innervation_mat.run
```

### Figures from dataset 05_: <span id="05"><span>

<p align="center">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_05.png">
</p>

#### FigS7: ANs that are active off of the spherical treadmill <span id="FigS7"><span>
```bash
$ ./_05-0-plot_FigS7-offBall_onBall_comparison.run
```
### Figures from dataset 06_: <span id="06"><span>

<p align="center">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_06.png">
</p>

####  FigS6: ANs from SS36112 respond to both air and CO2 puff <span id="FigS6"><span>
```bash
$ ./_06-0-plot_FigS6-Plot_air_vs_CO2puff.run
```

### Figures from dataset 07_: <span id="07"><span>

<p align="center">
  <img align="center" width="240" src="/images/Code_overflow_git_w_data_07.png">
</p>

#### Fig10b_left: Summary of neural activity of each PE during PE train <span id="Fig10b_left"><span>
```bash
$ ./_07-0-plot_Fig10b_left-DFF_per_PE.run
```












