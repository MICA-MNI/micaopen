# Structural MRI Analysis Pipeline

This directory contains scripts and instructions for processing and analyzing amygdala volumes from T1 nativepro maps.

## Steps

### 1. Segment Amygdala from T1 Nativepro Maps
Use volbrain.com to get segmentations of amygdala on T1 nativepro maps.

- **Input:** 
  - Brain T1 nativepro volume
- **Output:** 
  - Amygdala Mask

### register and process amygdala mask

- **2. Register Amygdala Segmentation to qT1 Space**
Get transformation matrix from nativepro T1 space to qT1map and bring amygdala segmentation into qT1 space.

- **3. Clean Resampled Mask Borders**
Clean resampled mask borders while overlayed on amygdala volume.

- **Input:** 
  - Amygdala Mask
  - Amygdala T1 volume
- **Output:** 
  - Amygdala Mask

**Tool:** `ITKSNAP`

- **4. Binarize Mask**
Binarize the mask and create separate masks for left and right amygdala.

### 5. Crop Amygdala Volumes
Crop the rest of the brain volume and crop mask so it is aligned and smaller.

### 6. Extract Radiomic Features
Extract features of the amygdala at all moments and kernel sizes.

- **Input:** 
  - Amygdala T1 volume
  - Amygdala mask
- **Output:** 
  - Feature maps

**Script:** `test_radiomics.ipynb`

### 7. Resample Radiomic Outputs
Resample all pyradiomics outputs to have the same dimensions as input.

### 8. Generate Feature Bank Figures
Make figures of the feature bank.

### 9. Create Feature Bank File
Make a feature bank dataframe from all the features for each subject as a feature bank (.csv)

- **Input:**
  - Feature maps
  - Amygdala mask
- **Output:** 
  - Feature bank

**Script:** `crop_featurebank.ipynb`

### 10. Generate UMAP Projections
With feature bank, get UMAP projection and save all embeddings as .csv.

- **Input:** 
  - Feature bank
- **Output:** 
  - UMAP embeddings

**Script:** `Umap_.ipynb`

### 11. Map U1 and U2 Values
Relate U1 and U2 values back to coordinate points to make maps for U1 and U2 in amygdala space.

### 12. Register U1 and U2 Maps to MNI152 Space
Register all the U1 and U2 maps of all 10 subjects into MNI152 space.

### 13. Correlate Aligned Maps
Calculate the correlations of all the aligned maps in MNI152 space with their coordinates (including BIGBRAIN). And creat a correlation table

### 14. Generate Radar Plots
Show correlations with the axes of BIGBRAIN and all the subjects as radar plots.

- **Input:** 
  - Correlation table
- **Output:** 
  - Correlation radar plot

**Script:** `radarplots.ipynb`

### 15. Variogram Matching Test
Conduct variogram matching test on all subject correlations of U1 and U2 to coordinate axes.

**Script:** `variograms-mni152.ipynb`

### 16. Functional Analysis
Continue to functional analysis found in the function folder

