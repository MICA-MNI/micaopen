# FROM HISTOLOGY TO MACROSCALE FUNCTION IN THE HUMAN AMYGDALA 

The following data demonstrates the workflow processes for analysis of the human amygdala. From histology and MRI microstructure to functional networks. The following steps outline the entire process.

## Prerequisites

- BigBrain volume and subcortical segmentations (Xiao 2019)
- Required software: Geany, MATLAB, Python, pyRadiomics, UMAP, etc.

# Amygdala Volume Analysis Pipeline

This repository contains scripts and instructions for processing and analyzing amygdala volumes from BIGBRAIN data.

## Steps

### 1. Crop Amygdala Volumes
Crop amygdala volumes from BIGBRAIN on each side of the brain, then resample mask to fit with cropped volumes, and binarize mask.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/volumes/full8_${resHisto}um_optbal.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/segmentations/ICBM2009b_sym-SubCorSeg-${resHisto}um_bigbrain.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-clean_ero5.nii.gz`

**Script:** `create_amyg_masks.sh`

### 2. Binarize Mask
Binarize the amygdala mask.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-clean_ero5.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`

**Script:** `binarize_mask.m`

### 3. Extract Radiomic Features
Extract features of the amygdala at all moments and kernel sizes.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/original_firstorder_${moments}_${kernelsize}_ero5_1sd.nii.gz`

**Script:** `test_radiomics.ipynb`

### 4. Resample Radiomic Outputs
Resample all pyradiomics outputs to have the same dimensions as input.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/original_firstorder_${moments}_${kernelsize}_ero5_1sd.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/original_firstorder_${moments}_${kernelsize}_reshape_ero5_1sd.nii.gz`

**Script:** `merger_amyg.sh`

### 5. Generate Figures
Make figures of the feature bank matrix and image plots.

**Scripts:** 
- `build_fig.m`
- `place_fig.m`

### 6. Create Feature Bank
Make a feature bank with subsampling from mask made in preprocess_mask.m. Save a dataframe of all the moments (feature bank) as a pickle file.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/original_firstorder_${moments}_${kernelsize}_reshape.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/cropped_featurebank.csv`

**Script:** `crop_featurebank.ipynb`

### 7. Register Julich Probability Map
Get the Julich probability map as a target for UMAP projections.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/segmentations/juelich_nlin2icbm2009casym.nii`
  - `/host/percy/local_raid/hans/amyg/hist/segmentations/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/volumes/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii`
  - `/host/percy/local_raid/hans/amyg/hist/volumes/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c_brain.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/volumes/mni_icbm152_nlin_sym_09b/mni_icbm152_t1_tal_nlin_sym_09b.nii`
  - `/host/percy/local_raid/hans/amyg/hist/volumes/mni_icbm152_nlin_sym_09b/mni_icbm152_t1_tal_nlin_sym_09b_brain.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/prob_maps/tpl-bigbrain_desc-${subregion}_${side}_histological_100um_resample.nii.gz`

**Script:** `register_juelichAtlas_BB.sh`

### 8. Make Amygdala MPM
Create probabilistic maps for the amygdala.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/prob_maps/tpl-bigbrain_desc-${subregion}_${side}_histological_100um_resample.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${res}um_mpm_${side}_rescale.nii.gz`

**Script:** `make_amygdala_mpm.m`

### 9. Julich Threshold Probabilistic Maps
Apply thresholding to the probabilistic maps.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/prob_maps/tpl-bigbrain_desc-${subregion}_${side}_histological_100um_resample.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${res}um_mpm_${side}_um_prob_prctile_all_overlap.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${res}um_mpm_${side}_um_prob_prctile_probs${subregion}.nii.gz`

**Script:** `juelich_thresh_probmaps.m`

### 10. Generate UMAP Projections
Generate UMAP projections and save embeddings as .csv.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/cropped_featurebank.csv`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umUMAPembeddings_${side}_amyg_ero5_1sd.csv`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${res}um_mpm_${side}_um_prob_prctile_all_overlap.csv`

**Script:** `Umap_.ipynb`

### 11. Validate UMAP Projections
Validate UMAP projections with Julich probability maps and plot UMAP with the 3 amygdala subregions.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umUMAPembeddings_${side}_amyg_ero5_1sd.csv`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${res}um_mpm_${side}_um_prob_prctile_probs${subregion}.nii.gz`

**Script:** `UMAP_heatmap.ipynb`

### 12. UMAP Color Spectrum
Make UMAP projection with color spectrum over all the data points.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umUMAPembeddings_${side}_amyg_ero5_1sd.csv`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/2Dclrbar_UMAP_"+side+"_"+res+"um_ero5_1sd`

**Script:** `Umap_2Dclrbar.ipynb`

### 13. Create Feature Bank Matrices
Make matrices of the whole feature bank, also when ordered by U1 and U2 values. Output 3 png files of matrices to place in figure 1.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umUMAPembeddings_${side}_amyg_ero5_1sd.csv`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umfeatures_${side}/cropped_featurebank.csv`

**Script:** `make_matrices.m`

### 14. UMAP Amygdala Map
Show U1 and U2 of UMAP as a 3D amygdala (also make plot of the color spectrum from UMAP space pasted onto the amygdala coordinates). Output the maps of U1 and U2 in their respective amygdala coordinates.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umUMAPembeddings_${side}_amyg_ero5_1sd.csv`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${resHisto}um_mask-bin-vF_ero5.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/2Dclrbar_UMAP_"+side+"_"+res+"um_ero5_1sd`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${res}um_${u1/u2}_ero5_1sd.nii.gz`

**Script:** `U1U2amygMap.m`

### 15. Generate U1 and U2 Plots
Matlab script that makes plots and graphs of U1 and U2 data. Output 3D histogram plots of U1 and U2 values along all 3 axes of the amygdala and their correlation values.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${res}um_${u1/u2}_ero5_1sd.nii.gz`

**Script:** `U1U2_plots.m`

### 16. Create Table for Ridge Plot
Matlab script to create a table for easy input into `ridge_plot.R` script.

- **Input:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${resHisto}umUMAPembeddings_${side}_amyg_ero5_1sd.csv`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${res}um_${u1/u2}_ero5_1sd.nii.gz`
  - `/host/percy/local_raid/hans/amyg/hist/outputs/${res}um_mpm_${side}_um_prob_prctile${subregion}.nii.gz`
- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/outputs/amyg_${side}_${res}seg_table.csv`

**Script:** `make_R_table.m`

### 17. Generate Ridge Plots
Make ridge plots of U1 and U2 data in all 3 amygdala subdivisions. Output a ridge plot figure for left and right amygdala.

- **Output:** 
  - `/host/percy/local_raid/hans/amyg/hist/figures/ridge_plots.png`

**Script:** `ridge_plot.R`

### 18. Variogram Matching Test
Do variogram matching test to account for spatial autocorrelation.

**Script:** `Variograms.ipynb`

### 19. Register BigBrain to MNI152 Space
Bring BIGBRAIN to MNI152 space.

**Script:** `RegisterBigBrain_to_MNI152.sh`

### 20. In Vivo Structure Analysis
Continue with in vivo structure analysis using the provided script.

**Script:** `/host/percy/local_raid/hans/amyg/struct/scripts/everything_7T.sh`
