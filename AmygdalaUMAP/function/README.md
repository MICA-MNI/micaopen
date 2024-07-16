# Functional Analysis Workflow

This repository contains scripts and instructions for registering 7T amygdala masks defined in qT1 space to functional space and performing multiple functional analyses.

## Prerequisites

- Amygdala masks defined in qT1 space
- Yeo functional network parcellations (Yeo et al. 2011)
- Required software: Python v3.7

## Steps

### 1. Generate Mean fMRI Volume
Generate mean fMRI volume as NIfTI.

### 2. Register the amygdala masks and U1 map to functional space
Register the amygdala masks generated in qT1 space to functional space

### 3. Extract Timeseries
Extract the timeseries of each voxel in the newly registered amygdala mask in functional space.

### 4. Spike Regression
Clean off spikes from timeseries data

- **Input:** 
  - Isolated amygdala timeseries
- **Output:** 
  - Cleaned isolated amygdala timeseries
  
**Script:** `4.rsfmri_spike_regression.ipynb`

### 5. Extract Top and Bottom 25% of U1 and U2 Values
Extract top 25% and bottom 25% of U1 and U2 values in the timeseries. Show functional networks of both amygdala regions and whole amygdala. Run the t-tests and get p-values for the connections from amygdala to the whole hemisphere.

- **Input:** 
  - Amygdala timeseries
  - Yeo parcellations (Yeo et al. 2011)
- **Output:** 
  - Functional correlation matrices
  
**Script:** `5.rsfmri_cortical_corr.ipynb`

### 6. Translate Functional Correlations
Translate the functional correlations with cortex into the 7 Yeo functional networks and plot differences.

- **Input:** 
  - Amygdala timeseries
  - Yeo parcellations (Yeo et al. 2011)
- **Output:** 
  - Functional correlation matrices averaged within each yeo network
  
**Script:** `6.rsfmri_cortical_corr_yeo7.ipynb`

### 7. Meta-Analysis on Subjects
Run meta-analysis on whole amygdala and U1 defined regions of all subjects and plot table and spider graph of the top terms correlated to their coactivation maps.

- **Input:** 
  - Amygdala timeseries
  - Functional correlation matrices
- **Output:** 
  - List of terms from meta analysis
  
**Script:** `7.rsfmri_cortical_corr_meta_analysis.ipynb`
