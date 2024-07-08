# Functional Analysis Workflow

This repository contains scripts and instructions for bringing 7T amygdala masks from qT1 space to functional space and performing various functional analyses.

## Steps

### 1. Generate Mean fMRI Volume
Generate mean fMRI volume as NIfTI.

### 2. Apply Transform from qT1 to Functional Space for Nativepro Brain
Apply transform from qT1 to functional space for the nativepro brain.

### 3. Apply Transform for U1 and U2
Apply transform from qT1 to functional space for nativepro (new nativepro which is qT1 space/T1map) U1 and U2.

### 4. Create Functional Amygdala Mask
Make the U1 values that are non-zero into the amygdala mask in functional space to help improve interpolation differences between mask and U1/U2 maps when registering to functional space.

- Script: make_func_mask.m

### 5. Extract Timeseries
Extract the timeseries of each voxel in the amygdala mask in functional space.

### 6. Spike Regression
Clean off spikes from data using Python.

- Script: rsfmri_spike_regression.ipynb

### 7. Extract Top and Bottom 25% of U1 and U2 Values
Extract top 25% and bottom 25% of U1 and U2 values in the timeseries. Show functional networks of both amygdala regions and whole amygdala. Run the t-tests and get p-values for the connections from amygdala to the whole hemisphere.

- Script: rsfmri_cortical_corr.ipynb

### 8. Translate Functional Correlations
Translate the functional correlations with cortex into the 7 Yeo functional networks and plot differences.

- Script: rsfmri_cortical_corr_yeo7.ipynb

### 9. Meta-Analysis on Subjects
Run meta-analysis on subjects and plot table and spider graph of top correlated words.

- Script: rsfmri_cortical_corr_meta_analysis.ipynb
