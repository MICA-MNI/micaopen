---
title: "MPC"
author: "Casey Paquola"
e-mail: "casey.paquola [at] mail.mcgill.ca"
date: "21 September 2018"
output: html_document
urlcolor: blue
---

# Microstructure profile covariance (MPC) analysis
Welcome to the MPC package; a companion to our article "Emergence of macrolevel functional topography from microstructure profile covariance". Here, we present the three step procedure to construct individualised microstructure profile covariance networks.

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
Python (tested with 3.0)   
MATLAB (tested on 17b - https://www.mathworks.com/products/matlab.html)   
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

**02_myelinMaptoSurf.sh**: Compiles intensity values along intracortical surfaces from a myelin-sensitive volume.Requires conte69 resampled surfaces - can be found in the templates folder on the github repository.

**surfToMPC.m**: Matlab function that builds microstructure profiles and covariance matrices.

## Citing this resource
If you use this code, please cite our article (currently under review)
And direct the reader to the github repository: https://github.com/MICA-MNI/micaopen/MPC

## Extra features
Atlas for levels of laminar differentiation (a la Mesulam 2001)   
SJH 1012 parcellation scheme - vertex-wise on conte69 32k and freesurfer annotation on fsaverage7   
Scripts to conduct diffusion map embedding in MATLAB may be found in https://github.com/MICA-MNI/micaopen/diffusion_map_embedding      

```
