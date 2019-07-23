
# A Moment of Change analysis
This repository is a companion to our article "A Moment of Change: Shifts in myeloarchitecture characterise adolescent development of cortical gradients". Here, we provide preprocessed data used in the analysis as well as the script to reproduce the primary figures. 

## How to run
The primary analysis is laid out in a the matlab script - reproduction_script.m (tested in 2017b and 2018a)
The raw data may not be released at this time due to ethics requirements, so we have attached preprocessed node-wise microstructure profiles for each subject included in the study, alongside basic anonymised demographic information.
The script requires SurfStat (http://www.math.mcgill.ca/keith/surfstat/) as well as the MPC, diffusion embedding and surfstat addons that are all housed in the larger micaopen repository. We recommend starting by cloning this repository and running through the main script step by step.
Figure 3 and small sections of Figure 1 were generated in R, whereby data is exported from matlab and then reformatted in R to suit the specific needs. We have signalled this where possible in the main script.

## How to cite
If you use this code, please cite our article:  Paquola & Bethlehem et al., 2019 bioRix ...
And direct the reader to the github repository: https://github.com/MICA-MNI/micaopen/tree/master/a_moment_of_change
            

    
            