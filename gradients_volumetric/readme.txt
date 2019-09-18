The gradients contained within this repo were created as part of Paquola et al., (2019), then projected to volumetric space.

The procedure used a subset of participants of the Human Connectome Project (n=110) and involved:
1) Downsample BOLD timeseries and microstructure profiles to 10000 vertices across the cortical mantle
2) Construct group-level functional connectivity (FC) and microstructure profile covariance (MPC) matrices
3) Transform to normalised angle matrices and apply diffusion map embedding to resolve the principle gradients
4) Project the gradient values from 10k vertices to MNI152 volume space using mri_surf2vol (Freesurfer tool)

