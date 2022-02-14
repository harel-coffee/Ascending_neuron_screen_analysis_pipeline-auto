# Ascending neuron screen analysis pipeline
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)

This repository is used to generate the figures published in the paper-- [**Ascending neurons convey behavioral state to integrative sensory and action selection centers in the brain**]().

This pipeline was developed and run on Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-76-generic x86_64). 
 
## Content
- [Installation](#installation)
- [Download preprocessed experimental data](#Download-preprocessed-experimental-data)
- [Reproducing the figures](#reproducing-the-figures)
 

## Installation
To be able to run all the script, Python and R have to be installed.

To intall the environment with specific versions of requried Python packages, please install Anaconda first if you haven't already. 

Install Anaconda --> https://www.anaconda.com/
### 1. Install the Python environment ```AN``` to run ```.py``` scripts by following the instructions below:
Clone repository:
```bash 
$ cd ../to/where/you/want/
$ git clone https://github.com/NeLy-EPFL/Ascending_neuron_screen_analysis_pipeline.git
```
Change the directory to your ```../Ascending_neuron_screen_analysis_pipeline``` folder where ```AN_env_public.yml``` is located:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline
```
Install the ```AN``` Python environment with packages in ```AN_env_public.yml```:
```bash
$ conda env create -f AN_env_public.yml
```
 


### 2. Install the CPU version of DeepLabCut used in this manuscript in its own environment (make sure to leave the ```AN``` environment using ```conda deactivate``` before performing the following steps)
Download and install DeepLabCut:
```bash
$ git clone git+https://github.com/DeepLabCut/DeepLabCut.git@413ae5e2c410fb9da3da26c333b6a9b87ab6c38f#egg=deeplabcut
```
Change the directory to ```/conda-environments``` where the ```DLC-CPU.yaml``` is located:
```bash
$ cd ../../DeepLabCut/conda-environments
```
Create the DLC-CPU environment and install the CPU version of DeepLabCut:
```bash
$ conda env create -f DLC-CPU.yaml
```
Now DeepLabcut should be installed and ready to use.


### 3. Install R and its associated packages
We use R 3.6.1 for some of the anaylsis pipeline. You can find more information about R [here](https://stat.ethz.ch/pipermail/r-announce/2019/000643.html).

Install R version 3.6.1 (2019-07-05) and the r-base-dev package to compile R packages:
```bash
$ sudo apt-get update 
$ sudo apt-get install r-base-dev=3.6.1
```

Launch R to install associated packages by entering ```R``` in the terminal:
```bash
$ R
```
Then install the R packages for this manuscript:
```R
> install.packages("ggpmisc")
> install.packages("ggplot2")
> install.packages("tidyverse")
> install.packages("tidyr")
> install.packages("dplyr")
> install.packages("reshape2")
```

**Optional**

Now the ```AN``` conda environment, DeepLabCut, and R should be installed.
If you want to check Python scripts seperately, remember to activate the ```AN``` environment manually before running each ```.py``` script:
```bash
$ source activate AN
$ python name.py
```

If you want to use DeepLabCut independently, remember to activate the DLC-CPU environment manually before running the script:
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
Download the data from [Harvard dataverse](https://dataverse.harvard.edu/dataverse/AN) and make sure that the location of the data inside each numbered folder is organized as it is below:

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

**Note:** Before running the following scripts, make sure that the Python environment and R packages are installed (see the Installation guide above).
To start running the analysis pipeline, execute the following ```.run``` script from the folder ```Ascending_neuron_screen_analysis_pipeline/scripts_for_public/```:
```bash
$ cd ../../Ascending_neuron_screen_analysis_pipeline/scripts_for_public/
```
Execute the script by typing ```./``` before the script fileame. For example:
```bash
$ ./_00-0-plot_FigS1-exemplar_DLC_proboscisLabel_PEevt_detection.run
```
The intermediate results must be generated in the order shown below to generate plots. Please check the diagram in each session that depicts the workflow from a particular input dataset to specific ouput plots. 

### Content
- [Figures from dataset 00_](#00):
  - [FigS1: Semi-automated detection of proboscis extensions](#FigS1)

- [Figures from dataset 00_, 01_ and 03_](#00-01-03):
  - [Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a: Prediction of neural activity](#Fig4a-Fig5a-Fig6a-Fig7b-Fig8a-Fig9a-Fig10a)
  - [Fig7c: Prediction of neural activity differences between left and right neurons due to turning](#Fig7c)
  - [Fig10b_right, Fig10c: Prediction of neural activity from convolved PEs](#Fig10b_right-Fig10c)
  - [FigS10: Behavior classifier confusion matrix](#FigS10)
  - [Fig2, FigS4 top: GLM of joint angle, leg, leg pair, and behavior for predicitng neural activity](#Fig2-FigS4-top)
  - [Fig7a: Explained variance matrix of turning for predicting neural activity](#Fig7a)

- [Figures-from-dataset-03_](#03):
  - [FigS2: Joint angle and behavior covariance matrix](#figS2)
  - [FigS3: Behavioral event-triggered average neural activity](#FigS3)
  - [Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b: Behavioral event-triggered average neural activity](#Fig4b-Fig5b-Fig6b-Fig7b-Fig8b-Fig9b)
  - [Fig6c, Fig7e: Neural activity related ball rotations](#Fig6c-Fig7e)
  - [FigS5: ANs from SS36112 respond to puff stimulation rather than backward walking](#FigS5)

- [Figures-from-dataset-04_](#04):
  - [Fig3, FigS4: Large-scale anatomical quantification of ascending neuron projections to the brain and ventral nerve cord](#Fig3-FigS4)

- [Figures-from-dataset-05_](#05):
  - [FigS7: ANs that are active for movements off of the spherical treadmill](#FigS7)

- [Figures-from-dataset-06_](#06):
  - [FigS6: ANs from SS36112 respond to puffs of either air or CO2](#FigS6)

- [Figures-from-dataset-07_](#07):
  - [Fig10b_left: Summary of neural activity for each PE during PE trains](#Fig10b_left)





### Figures from dataset 00_: <span id="00"><span>
 
<p align="left">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_00.png">
</p>
 
#### FigS1: Semi-automated detection of proboscis extensions <span id="FigS1"><span>
```bash
$ ./_00-0-plot_FigS1-exemplar_DLC_proboscisLabel_PEevt_detection.run
```
Outputs:
```/output/FigS1-exemplar_PEevt_detection/```



### Figures from datasets 00_, 01_, and 03_: <span id="00-01-03"><span>

<p align="left">
  <img align="center" width="780" src="/images/Code_overflow_git_w_data_00_01_03.png">
</p>

The intermediate file must first be generated:
```bash
$ ./_00_01_03-1_train_behavior_classifier.run
$ ./_00_01_03-2_predict_behavior_and_sync_beh_w_DFF.run
```
Outputs:
```/output/Fig2_S4-GLM_jangles_legs_beh_DFF/```
 

***Note: The intermediate resuls from the behavior classifier and synchronized dataframes can now be substituted with the those used in this work from*** ```/02_Fig2_output_of_published_version``` ***if you want to skip*** ```_00_01_03-1_train_behavior_classifier.run.run``` and ```_00_01_03-2_predict_behavior_and_sync_beh_w_DFF.run```.

 
Once the intermediate results are generated, the following plots can be made using the following bash scripts:
 
#### Fig4a, Fig5a, Fig6a, Fig7b, Fig8a, Fig9a, Fig10a: Prediction of neural activity <span id="Fig4a-Fig5a-Fig6a-Fig7b-Fig8a-Fig9a-Fig10a"><span>
```bash
$ ./_00_01_03-2-plot_Fig4a_5a_6a_7b_8a_9a_10a-Plot_prediction_rawDFF_traces.run
```
Outputs:
```/output/Fig4a5a6a7b8a9a10a-representativeDFF_traces/```
 
#### Fig7c: Prediction of neural activity differences between left and right ANs is associated with turning <span id="Fig7c"><span>
```bash
$ ./_00_01_03-2-plot_Fig7c-Plot_dDFF_traces_fit_turning.run
```
Outputs:
```/output/Fig7a_7c-turning/```
 
#### Fig10b_right, Fig10c: Prediction of neural activity from convolved PEs <span id="Fig10b_right-Fig10c"><span>
```bash
$ ./_00_01_03-2-plot_Fig10b_right_10c-Plot_convPE.run
```
Outputs:
```/output/Fig10a_10c-PE_analysis/```
 
#### FigS10: Behavior classifier confusion matrix <span id="FigS10"><span>
```bash
$ ./_00_01_03-2-plot_FigS10-beh_jangle_confusionMat.run
```
Outputs:
```/output/FigS10-confusionMat_beh_classifier/```



#### Fig2, FigS4 top: GLM of joint angle, leg, leg pair, and behavior for predicting neural activity <span id="Fig2-FigS4-top"><span>
To plot and visualize the GLM matrix, the following intermediate GLM results must first be generated:
```bash
$ ./_00_01_03-3_glm_of_beh_leg_legPair_jangle_DFF.run
```
***Note: GLM intermediate results used in this paper can be found in four*** ```/02_Fig2_output_of_published_version/overview_...``` ***folders. Use them if you want to skip this GLM step***
 
Then, plot with:
```bash
$ ./_00_01_03-3-plot_Fig2abcd_S4-Plot_glmmat_of_beh_leg_legPair_jangle_DFF.run
```
Outputs:
```/output/Fig2_S4-GLM_jangles_legs_beh_DFF/```

#### Fig7a: Explained variance matrix of turning in predicitng neural activity <span id="Fig7a"><span>
To visualize and plot the turning R-squared matrix, the following intermediate results must first be generated:
```bash
$ ./_00_01_03-4_turn_mat_analysis.run
```
Then, plot using:
```bash
$ ./_00_01_03-4-plot_Fig7a-Plot_turn_analysis_matrix.run
```
Outputs:
```/output/Fig7a_7c-turning/```

### Figures from dataset 03_: <span id="03"><span>

<p align="left">
  <img align="center" width="600" src="/images/Code_overflow_git_w_data_03.png">
</p>

#### FigS2: Joint angle and behavior covariance matrix <span id="FigS2"><span>
```bash
$ ./_03-0-plot_FigS2-jangle_beh_covariance.run
```
Outputs:
```/output/FigS2-jangle_beh_covariance/```

#### FigS3: Behavioral event-triggered average neural activity <span id="FigS3"><span>
First the intermediate results of averaging neural activity for each behavioral epoch need to be generated:
```bash
$ ./_03-1_prep_DFF_beh_mat.run
```
Then, the results can be visualized using the following scripts:
```bash
$ ./_03-2-plot_FigS3-Plot_DFFmat.run
```
Outputs:
```/output/FigS3-DFF_mat/```

#### Fig4b, Fig5b, Fig6b, Fig7b, Fig8b, Fig9b: Behavioral event-triggered average neural activity <span id="Fig4b-Fig5b-Fig6b-Fig7b-Fig8b-Fig9b"><span>
```bash
$ ./_03-2-plot_Fig4b_5b_6b_7d_8b_9b-Plot_BehEvt_avgDFF.run
```
Outputs:
```/output/Fig4b_5b_6b_7e_8b_9b-Beh_avgDFF/```

#### Fig6c, Fig7d: Neural activity-associated ball rotations <span id="Fig6c-Fig7e"><span>
Intermediate results of neural event detection first need to be generated:
```bash
$ ./_03-3_prep_DFFevt_analysis.run
```
Then, the results can be visualized using the following scripts:
```bash
$ ./_03-3-plot_Fig6c_7e-Plot_DFFevt_analysis.run
```
Outputs:
```/output/Fig6c_7e-DFF_event_corresponding_ballRot/```

#### FigS5: ANs from SS36112 respond to puff stimulation rather than backward walking <span id="FigS5"><span>
Intermediate results of puff and backward walking event detection first need to be generated:
```bash
$ ./_03-4_prep_SS36112_independentBW_vs_CO2puffBW_analysis.run
```
Then, the results can be visualized using the following scripts:
```bash
$ ./_03-4-plot-FigS5-SS36112_independentBW_vs_CO2puffBW_analysis.run
```
Outputs:
```/output/FigS5-CO2puff_BW_analysis_SS36112/```
 

### Figures from dataset 04_: <span id="04"><span>

<p align="left">
  <img align="center" width="220" src="/images/Code_overflow_git_w_data_04.png">
</p>


#### Fig3, FigS4: Large-scale anatomical quantification of ascending neuron projections to the brain and ventral nerve cord <span id="Fig3_ FigS4"><span>

Intermediate results of puff and backward walking event detection first need to be generated:
```bash
$ ./_04-1_prep_singleAN_innervation_mat.run
```
Then, the results can be visualized using the following scripts:
```bash
$ ./_04-1-plot_Fig3_S4-Plot_singleAN_innervation_mat.run
```
Outputs:
```/output/Fig3_S4-single_AN_innervation_mat/```
 
### Figures from dataset 05_: <span id="05"><span>

<p align="left">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_05.png">
</p>

#### FigS7: ANs that are active during movements off of the spherical treadmill <span id="FigS7"><span>
```bash
$ ./_05-0-plot_FigS7-offBall_onBall_comparison.run
```
Outputs:
```/output/FigS7-offballActive_ANs/```

### Figures from dataset 06_: <span id="06"><span>

<p align="left">
  <img align="center" width="200" src="/images/Code_overflow_git_w_data_06.png">
</p>

####  FigS6: ANs from SS36112 respond to puffs of either air or CO2 <span id="FigS6"><span>
```bash
$ ./_06-0-plot_FigS6-Plot_air_vs_CO2puff.run
```
Outputs:
```/output/FigS6-air_vs_CO2_puff_comparison/```

### Figures from dataset 07_: <span id="07"><span>

<p align="left">
  <img align="center" width="255" src="/images/Code_overflow_git_w_data_07.png">
</p>

#### Fig10b_left: Summary of neural activity during each PE of a PE train <span id="Fig10b_left"><span>
```bash
$ ./_07-0-plot_Fig10b_left-DFF_per_PE.run
```
Outputs:
```/output/Fig10b_left-PE_dynamic/```











