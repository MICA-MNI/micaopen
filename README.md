# micaopen

Open Software from the MICA lab (http:/mica-mni.github.io), other useful tools, and supplementary data that accompanies some of our recent publications. 

## Main tools 
_MPC_: tool for microstructure profile covariance analysis, which can generate subject specific networks from histological reconstructions as well as myelin sensitive MRI data, used for the analysis of microstructural gradients. For further details, see our paper: Paquola et al. 2019 PLoS Biology (https://doi.org/10.1371/journal.pbio.3000284)

gradients_volumetric: The gradients contained within this repo were created as part of Paquola et al.(2019) then projected to volumetric MNI152 space for wider use. 

BigBrain: BigBrain histological profiles and statistical profile moments. Please cite Paquola et al., (2019) when using the Big Brain profiles (https://doi.org/10.1371/journal.pbio.3000284)

BrainSpace: BrainSpace is a lightweight cross-platform toolbox primarily intended  for macroscale gradient mapping and analysis of neuroimaging and connectome level data. BrainSpace is available in Python and MATLAB. For further details, see Vos de Wael R, Benkarim O, et al. (2019) biorxiv (https://www.biorxiv.org/content/10.1101/761460v) and http://brainspace.readthedocs.io

diffusion_map_embedding: this code implements diffusion map embedding technique in Matlab, used in our hippocampal subfield connectivity gradient paper: Vos de Wael et al., 2018 PNAS (https://www.pnas.org/content/115/40/10154.abstract). These tools have now become part of BrainSpace, see above link. 

a_moment_of_change: This repository is a companion to our preprint "A Moment of Change: Shifts in myeloarchitecture characterise adolescent development of cortical gradients" (https://www.biorxiv.org/content/10.1101/706341v2). In the repo, we provide preprocessed data used in the analysis as well as the script to reproduce the primary figures 

SurfStat: Contains SurfStat (Chicago version) for surface- and volume-based statistical analysis and visualization. Documentation links are here: http://math.mcgill.ca/~keith/surfstat or http://mica-mni.github.io/surfstat. Also contains addons from the micalab and tutorial data. 



## Other goodies 
mica_powertools: extra scripts from the MICA lab, loosely documented at this point but perhaps soon unified, better documented, and toolboxed

dcm_sorter - python code to sort a dicom directory into subfolders 

autism_hierarchy: videos of step wise functional connectivity analysis performed in connectome manifolds. For furter detauks see Hong et al., 2019 Nat Comms, link here https://www.nature.com/articles/s41467-019-08944-1

The  micaopen tools result from the dedication and collaboration of all members of the lab, notably Casey Paquola, Reinder Vos de Wael, Oualid Benkarim, Sara Lariviere, Raul Cruces, Bo-Yong Park, Jessica Royer, Seok-Jun Hong, and Boris Bernhardt.
