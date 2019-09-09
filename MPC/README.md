---
title: "MPC"
author: "Casey Paquola"
e-mail: "casey.paquola@mail.mcgill.ca"
date: "21 September 2018"
output: html_document
urlcolor: blue
---

# Microstructure profile covariance (MPC) analysis
Welcome to the MPC package; a companion to our article "Microstructural and functional gradients are increasingly dissociated in transmodal cortices". Here, we present the three step procedure to construct individualised microstructure profile covariance networks.

### Table of contents
* [Software dependencies](#software-dependencies)   
* [Preprocessing](#preprocessing)   
* [File and folder structure](#file-and-folder-structure)   
* [Step by step guide](#step-by-step-guide)   
* [Citing this resource](#citing-this-resource)   
* [Extra features](#extra-features)   

## Software dependencies
Freesurfer (tested with 5.1 - https://surfer.nmr.mgh.harvard.edu/)   
FSL (tested with 5.0 - https://fsl.fmrib.ox.ac.uk/fsl/fslwiki)   
Python (tested with 2.7 and 3.6)   
MATLAB (tested on 17b and 16a - https://www.mathworks.com/products/matlab.html)   
SurfStat (http://www.math.mcgill.ca/keith/surfstat/)   
surface_tools (https://github.com/kwagstyl/surface_tools)   

## Preprocessing
Prior to using this package it is expected that the individual scans have undergone recon-all processing with freesurfer, and a myelin-sensitive image has been constructed (ie: t1w/t2w, qt1, mt)

## File and folder structure
Our pipeline assumes a BIDS folder structure (http://bids.neuroimaging.io/)
Note: the output of recon-all is housed within the surfaces subfolder.
```{r, echo=TRUE}
# /Data/BIDS/   
#       .../subID/   
#             .../anat/  
#             .../func/  
#             .../dwi/   
#             .../fmap/   
#             .../surfaces/   
#                     .../subID/   
#                           .../label/   
#                           .../mri/   
#                           .../scripts/   
#                           .../stats/   
#                           .../surf/   
#                           .../tmp/   
#                           .../touch/   
#                           .../trash/   
#                   ...   
```   

## Step by step guide
Within the github repository are three scripts, which should be run in sequence. There are a few lines to hardcode in each script such as the path to your BIDS directory and subject list. These will be contained in the first few lines. The first two scripts operate through bash, while the third is operationalised within matlab. 

**01_constructSurfaces.sh**: Constructs equivolumetric intracortical surfaces using "surface tools" (https://github.com/kwagstyl/surface_tools)

**02_myelinMaptoSurf.sh**: Compiles intensity values along intracortical surfaces from a myelin-sensitive volume, and registers an annotation from fsaverage to the individual subject.

**03_surfToMPC.m**: Imports data to matlab and builds microstructure profile covariance matrices. Set up to be used with the 1012 parcellation scheme. An additional step of normalisation to a standard template is necessary for vertex-wise analyses. 

## Citing this resource
If you use this code, please cite our article:  Paquola et al., 2019 "Microstructural and functional gradients are increasingly dissociated in transmodal cortices" PLoS Biology 
And direct the reader to the github repository: https://github.com/MICA-MNI/micaopen/MPC

## Extra features
Atlas for levels of laminar differentiation (a la Mesulam 2001), 1-paralimbic, 2-hetermodal, 3-unimodal, 4-idiotypic, 0-cortical wall. 
  lh.mesulam.annot & rh.mesulam.annot on fsaverage7  
  mesulam_conte69.txt  

Atlas for cytoarchitectural complexity (Adler et al., 2018 Epilepsia)
  lh.economo.annot & rh.economo.annot on fsaverage7  
  economo_conte69.txt  

SJH 1012 parcellation scheme  
  lh.sjh.annot & rh.sjh.annot on fsaverage7  
  sjh_conte69.txt  

Principle gradient from the manuscript (G1-HIST and G1-MRI). G1_hist is derived from Big Brain (Figure 2) and was mapped to fsaverage5 and conte69 using nearest neighbour interpolation (improved methods for registration of Big Brain to these surfaces is upcoming and should be adopted in the future). G1_mri is derived from T1w/T2w imaging from the Human Connectome Project (Figure 3). 
  G1_hist_sjh_parcel_fsaverage7.txt  
  G1_hist_sjh_parcel_conte69.txt  
  G1_mri_sjh_parcel_fsaverage7.txt  
  G1_mri_sjh_parcel_conte69.txt  

Scripts to conduct diffusion map embedding in MATLAB may be found in https://github.com/MICA-MNI/micaopen/diffusion_map_embedding   

```
