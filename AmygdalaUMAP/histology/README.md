# Amygdala Microstructure Analysis Workflow

This workflow processes histological and MRI data to map variations in the regional microstructure of the amygdala. The following steps outline the entire process.

## Prerequisites

- BigBrain volume and subcortical segmentations (Xiao et al. 2019)
- Julich probability maps (Amunts et al. 2020)
- Required software: Python

# Amygdala Volume Analysis Pipeline

This repository contains scripts and instructions for processing and analyzing amygdala volumes from BIGBRAIN data.

## Steps

### Isolate and prep Amygdala volume from BIGBRAIN

- **1. Crop Amygdala Volumes**
Crop amygdala volumes from BIGBRAIN on each side of the brain, then resample mask to fit with cropped volumes

- **2. Binarize Mask**
Binarize the amygdala mask.

**Script:** `binarize_mask.m`

### 3. Extract Radiomic Features
Extract features of the amygdala at all moments and kernel sizes.

- **Input:** 
  - Amygdala Mask
  - BIGBRAIN volume
- **Output:** 
  - 20 different features

**Script:** `test_radiomics.ipynb`

### Align and process feature maps

- **4. Resample Radiomic Outputs**
Resample all pyradiomics outputs to have the same dimensions as origianl BIGBRAIN volume

### 6. Create Feature Bank Matrix
Put all the features into a pandas dataframe of all the moments (feature bank).

- **Input:** 
  - Feature volumes
- **Output:** 
  - .csv file of feature bank

**Script:** `crop_featurebank.ipynb`

### Retrieve and process Juelich probability maps of amygdala

- **7. Generate Julich Probability Maps**
Get the Julich probability map as a target for UMAP projections

- **8. Register Julich Probability Maps**
Register probabilistic maps to correct space.

- **9. Julich Threshold Probabilistic Maps**
Apply thresholding to the Juelich probability maps.

### 10. Generate UMAP Projections
Generate UMAP projections

- **Input:** 
  - Amygdala mask
  - BIGBRAIN volume
  - Feature bank
- **Output:** 
  - UMAP embeddings
  - Juelich Probability maps
  
**Script:** `Umap_.ipynb`

### 11. Validate UMAP Projections
Validate UMAP projections with thresholded Julich probability maps and plot UMAP with the 3 amygdala subregions.

- **Input:** 
  - Amygdala mask
  - UMAP embeddings
  - Juelich Probability maps

**Script:** `UMAP_heatmap.ipynb`

### 12. UMAP Color Spectrum
Apply color spectrum map over all the data points in UMAP projection.

- **Input:** 
  - Amygdala Mask
  - UMAP embeddings
- **Output:** 
  - UMAP colour spectrum embeddings

**Script:** `Umap_2Dclrbar.ipynb`

### Make plots of all results for Figure 1 of project

### 18. Variogram Matching Test
Do variogram matching test to account for spatial autocorrelation.

- **Input:** 
  - Amygdala Mask
  - UMAP embeddings
- **Output:** 
  - UMAP colour spectrum embeddings

**Script:** `Variograms.ipynb`

### 19. Register BigBrain to MNI152 Space
Bring BIGBRAIN to MNI152 space for translation to structural MRI

### 20. In Vivo Structure Analysis
Continue with in vivo structure analysis found in the Structure folder

