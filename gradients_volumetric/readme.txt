The gradients contained within this repo were created as part of Paquola et al., (2019) then projected to volumetric space for wider use.
https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000284#sec025

The procedure used a subset of participants of the Human Connectome Project (n=110) and involved:
1) Group-level functional connectivity (FC) and microstructure profile covariance (MPC) matrices were constructed on a 10k cortical mesh
2) Matrices were transformed into normalised angle matrices and we applied diffusion map embedding to resolve the principle gradients
3) Gradient values were projected from 10k mesh to MNI152 volume space using mri_surf2vol (Freesurfer tool)

The volumetric template was MNI152_T1_2mm_brain.nii, which is provided in the standard atlases of FSL. 
