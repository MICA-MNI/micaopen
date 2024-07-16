# Structural MRI Analysis Pipeline

This directory contains scripts and instructions for processing and analyzing amygdala volumes from T1 nativepro maps and translating methods developed in histology.

## Prerequisites

- T1 nativepro maps of 10 different healthy subjects from the MICA-PNC dataset (Cabalo et al. 2024), and preprocessed through Micapipe (Cruces et al. 2022)
- Required software: Python v3.7, ITK-snap v3.8

## Steps

### 1. Segment Amygdala from T1 Nativepro Maps
Use volbrain.com (Manjon et al. 2016) to get segmentations of amygdala on T1 nativepro maps.

- **Input:** 
  - Brain T1 nativepro volume
- **Output:** 
  - Amygdala Mask

### Register and process amygdala mask

- **2. Register Amygdala Segmentation to qT1 Space**
Get transformation matrix from nativepro T1 space to qT1map and bring amygdala segmentation into qT1 space.
Note: transformation matrix can be generated using normalization tools such as ANTs (Avants et al. 2014).

- **3. Clean Resampled Mask Borders**
Clean and manually correct the resampled mask borders while overlayed on amygdala volume using ITK-Snap (Yushkevich et al. 2016)

**Tool:** `ITKSNAP v3.8`

- **4. Binarize Mask**
Binarize the mask and create separate masks files, separating the left and right amygdala.

- **5. Crop Amygdala Volumes**
Crop the rest of the brain volume and crop masks to make them aligned to amygdala volumes.

### 6. Extract Radiomic Features
Extract features of the amygdala at all moments and kernel sizes.

- **Input:** 
  - Amygdala T1 volume
  - Amygdala mask
- **Output:** 
  - Feature bank (n=20, 4 moments x 5 kernel sizes) for each of the 10 subjects

**Script:** `6.test_radiomics.ipynb`

### 7. Resample Radiomic Outputs
Resample all pyradiomics outputs to have the same dimensions as input. The dimensions of the PyRadiomics outputs always  get modified from its input, so we must realign the output volumes to their input volume.

### 8. Create Feature Bank File
Make a feature bank dataframe from all the features for each subject as a feature bank (.csv)

- **Input:**
  - Feature maps
  - Amygdala mask
- **Output:** 
  - Feature bank (.csv) for each of the 10 subjects

**Script:** `8.crop_featurebank.ipynb`

### 9. Generate UMAP Projections
With the feature bank, get UMAP projections and save all embeddings as .csv files

- **Input:** 
  - Feature bank
- **Output:** 
  - UMAP embeddings of feature bank (2 components)

**Script:** `9.Umap_.ipynb`

### Map embeddings to amygdala and align the two UMAP component (U1 and U2) maps of all subjects
- **10. Map U1 and U2 Values**
Relate U1 and U2 values back to coordinate points to make maps for U1 and U2 in the amygdala T1 nativepro space.

- **11. Register U1 and U2 Maps to MNI152 Space**
Register all the U1 and U2 maps of all 10 subjects into MNI152 space using tranformation matrices generated from ANTs  (Avants et al. 2014).

- **12. Correlate Aligned Maps**
Calculate the correlations of all the aligned maps in MNI152 space with their coordinates (including BIGBRAIN). Then create a correlation table with the correlations values of the Inferior-Superior, Medial-Lateral and Anteriror-Posterior to the U1 and U2 UMAP components.

### 13. Generate correlation spider plots
Show correlations with the axes of BIGBRAIN and all the subjects as radar plots.

- **Input:** 
  - Correlation table
- **Output:** 
  - Correlation radar plot

**Script:** `13.radarplots.ipynb`

### 15. Variogram Matching Test
Apply variogram matching test to account for spatial autocorrelation in correlating U1 and U2 with all three coordinate axes on all 10 subjects.

- **Input:** 
  - Amygdala Mask
  - UMAP embeddings
- **Output:** 
  - Histogram and p-values of variogram null model

**Script:** `14.variograms-mni152.ipynb`

### Functional Analysis
Continue with functional analysis found in the function folder

