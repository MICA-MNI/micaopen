# Structural MRI Analysis Pipeline

This repository contains scripts and instructions for processing and analyzing amygdala volumes from T1 nativepro maps.

## Steps

### 1. Segment Amygdala from T1 Nativepro Maps
Use brainvol to get segmentations of amygdala on T1 nativepro maps.

- **Input:** 
  - `/data_/mica3/BIDS_PNC/derivatives/micapipe/sub-${sub}/ses-${ses}/anat/sub-${sub}_ses-${ses}_space-nativepro_t1w.nii.gz`
- **Output:** 
  - `/data_/mica1/03_projects/hans/7T/outputs/PNC00X_seg/native_lab_n_mmni_fjob398136.nii`

### 2. Register Amygdala Segmentation to qT1 Space
Get transformation matrix from nativepro T1 space to qT1map and bring amygdala segmentation into qT1 space.

- **Input:** 
  - `/data_/mica3/BIDS_PNC/derivatives/micapipe/sub-${sub}/ses-${ses}/anat/sub-${sub}_ses-${ses}_space-nativepro_t1w.nii.gz`
  - `/data_/mica3/BIDS_PNC/rawdata/sub-${sub}/ses-${ses}/anat/sub-${sub}_ses-${ses}_acq-inv1_T1map.nii.gz`
  - `/host/percy/local_raid/hans/amyg/struct/outputs/native_lab_n_mmni_fjob398136.nii`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${sub}_${ses}_subCor_seg_T1mapSpace.nii.gz`

**Script:** `get_registrations.sh`

### 3. Clean Resampled Mask Borders
Clean resampled mask borders while overlayed on amygdala volume.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/PNC00#_seg/subCor_seg_T1mapSpace.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/PNC00#_seg/subCor_seg_T1mapSpace.nii.gz`

**Tool:** `ITKSNAP`

### 4. Binarize Mask
Binarize the mask and create separate masks for left and right amygdala.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/PNC00#_seg/subCor_seg_T1mapSpace.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_mask_${sub}_${ses}_${side}.nii.gz`

**Script:** `binarize_mask.m`

### 5. Crop Amygdala Volumes
Crop the rest of the brain volume and crop mask so it is aligned and smaller.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_mask_${sub}_${ses}_${side}.nii.gz`
  - `/data_/mica3/BIDS_PNC/rawdata/sub-${sub}/ses-${ses}/anat/sub-${sub}_ses-${ses}_acq-T1_T1map.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_mask_${sub}_${ses}_${side}_roi.nii.gz`
  - `/host/percy/local_raid/hans/amyg/struct/volumes/amyg_${sub}_${ses}_${side}_vol.nii.gz`

**Script:** `segment_amyg_7T.sh`

### 6. Extract Radiomic Features
Extract features of the amygdala at all moments and kernel sizes.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_${sub}_${ses}_${side}.nii.gz`
  - `/host/percy/local_raid/hans/amyg/struct/volumes/amyg_${sub}_${ses}_${side}_vol.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${sub}_${ses}features/original_firstorder_${moments}_${kernelsize}.nii.gz`

**Script:** `test_radiomics.ipynb`

### 7. Resample Radiomic Outputs
Resample all pyradiomics outputs to have the same dimensions as input.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${resHisto}umfeatures_${side}/original_firstorder_${moments}_${kernelsize}.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${resHisto}umfeatures_${side}/original_firstorder_${moments}_${kernelsize}_reshape.nii.gz`

**Script:** `merger_amyg7T.sh`

### 8. Generate Feature Bank Figures
Make figures of the feature bank.

**Scripts:** 
- `build_fig_7T.m`
- `place_fig_7T.m`

### 9. Create Feature Bank File
Make a feature bank file from all the features for each subject and save a dataframe of all the moments (feature bank) as a CSV file.

- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${resHisto}umfeatures_${side}/cropped_featurebank.csv`

**Script:** `crop_featurebank.ipynb`

### 10. Generate UMAP Projections
With feature bank, get UMAP projection and save all embeddings as .csv. Also load Julich probability maps to add to UMAP projections.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${resHisto}umfeatures_${side}/cropped_featurebank.csv`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${resHisto}umUMAPembeddings_${side}/*.csv`

**Script:** `Umap_.ipynb`

### 11. Map U1 and U2 Values
Relate U1 and U2 values back to coordinate points to make maps for U1 and U2.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_${sub}_01_${side}_roi.nii.gz`
  - `/host/percy/local_raid/hans/amyg/struct/outputs/${resHisto}umUMAPembeddings_${side}/*.csv`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_${sub}_01_${side}_u1.nii.gz`
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_${sub}_01_${side}_u2.nii.gz`

**Script:** `U1U2amyg_map_7T.m`

### 12. Register U1 and U2 Maps to MNI152 Space
Get all the U1 and U2 maps into MNI152 space.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/amyg_${sub}_01_${side}_u2/1.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/registration/${sub}_${ses}_${side}_amyg_u2/1_MNI152Space_1sd.nii.gz`

**Script:** `get_registrations_qT1-MNI152.sh`

### 13. Correlate Aligned Maps
Get the correlations of all the aligned maps in MNI152 space with their coordinates (including BIGBRAIN).

- **Output:** 
  - `/host/percy/local_raid/hans/amyg/struct/outputs/corr_subs_${side}_1sd.csv`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/corr_MNI152_${side}_1sd.csv`

**Script:** `U1U2_plots_7T_corr.m`

### 14. Generate Radar Plots
Show the correlations with the axes of BIGBRAIN and all the subjects in radar plots.

**Script:** `radarplots.ipynb`

### 15. Variogram Matching Test
Get the variogram matching values of all the subjects.

**Script:** `variograms-mni152.ipynb`

### 16. Functional Analysis
Continue with functional analysis using the provided script.

**Script:** `/host/percy/local_raid/hans/amyg/func/scripts/everything_func_new.sh`
