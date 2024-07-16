# Functional analysis workflow

This repository contains scripts and instructions for registering 7T amygdala masks defined in native space quantitative T1 to functional space and performing multiple functional analyses.

## Prerequisites

- Amygdala masks defined in qT1 space (from structural module)
- Yeo functional network parcellations (Yeo et al. 2011)
- Required software: Python v3.7

## Steps

### Register amygdala masks to functional space and extract timeseries
**1. Generate mean fMRI Volume**: Generate mean fMRI volume as NIfTI.

**2. Register the amygdala masks and U1 map to functional space**: Register the amygdala masks generated in qT1 space to functional space

**3. Extract timeseries**: Extract the timeseries of each voxel in the newly registered amygdala mask in functional space.

### Spike regression
**4. Preprocess timeseries by cleaning off irregularities (spikes) from timeseries data**

- **Input:** 
  - Isolated amygdala timeseries
- **Output:** 
  - Cleaned amygdala timeseries
  
**Script:** `4.rsfmri_spike_regression.ipynb`

### Extract top and bottom 25% of U1 and U2 values
**5. Extract top 25% and bottom 25% of U1 and U2 values in the timeseries:** Show functional networks of both amygdala regions and whole amygdala. Run the t-tests and get p-values for the correlations between the amygdala and the whole cortex.

- **Input:** 
  - Amygdala timeseries
  - Cortical template (fs-LR)
- **Output:** 
  - Functional correlation matrices (python plot)
  
**Script:** `5.rsfmri_cortical_corr.ipynb`

### Translate functional correlations
**6. Translate the functional correlations:** Once cortical correlations are generated, average all values within each of the 7 Yeo functional networks and plot the differences between networks.

- **Input:** 
  - Amygdala timeseries
  - Yeo parcellations (Yeo et al. 2011)
- **Output:** 
  - Functional correlation matrices averaged within each yeo network (python plot)
  
**Script:** `6.rsfmri_cortical_corr_yeo7.ipynb`

### Meta-analysis on subjects
**7. Run meta-analysis on all the computed cortical correlation maps:** Meta-analysis is run on cortical correlations maps of the whole amygdala, the two U1 defined regions and the difference of high and low U1 value regions. Plot a table and spider graph of the top terms correlated to their coactivation maps.

- **Input:** 
  - Amygdala timeseries
  - Functional correlation matrices
- **Output:** 
  - List of terms from meta analysis (.csv)
  
**Script:** `7.rsfmri_cortical_corr_meta_analysis.ipynb`
