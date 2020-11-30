.. role:: matlab(code)
   :language: matlab

Temporal Gradient Figures
____________________________________
.. image:: figure.png
    :width: 400px

This is the code accompanying the manuscript `Microstructural underpinnings and macroscale functional implications of temporal lobe connectivity gradients <https://www.biorxiv.org/content/10.1101/2020.11.26.400382v1>`_. It will allow you to reproduce the main figures of the manuscript. The development version of the `BrainSpace toolbox <https://brainspace.readthedocs.io/>`_ is required for running the code herein. 

Usage
=============
First, make sure to add this toolbox and the BrainSpace development version to your MATLAB path:

.. code-block:: matlab
    addpath(gepnath('/path/to/micaopen/temporal_gradients'))
    addpath(genpath('/path/to/brainspace/matlab'))

Next, you can download the required data by running :matlab:`temporal_gradients.download_data`. The plots for, for example figure 1, can be produced by running :matlab:`temporal_gradients.master_figure1`. The resulting figures will be stored in the directory micaopen/temporal_gradients/+temporal_gradients/figures/figure1. 

Data
===============

The function :matlab:`temporal_gradients.download_data` will automatically download a data file called figure_data.mat and store it inside :matlab:`micaopen/temporal_gradients/+temporal_gradients/data`. The contents of `figure_data.mat` are as follows:

 - bigbrain: the MPC gradients
 - c69_20k: structure containing conte69 surfaces downsampled to 20000 vertices, indices for the downsampling, and a midline mask.
 - connectivity_distance: connectivity distance of the temporal lobe
 - connectivity_vector_3829: connectivity of the left temporal pole (vertex 3829)
 - evo_data: functional homology index and cortical expansion of the temporal lobe.
 - gm_hcp_discovery: GradientMaps object of the discovery dataset.
 - gm_hcp_replication: GradientMaps object of the replication dataset.
 - gm_mics: GradientMaps object of the MICS dataset.
 - include: vertices included in the yeo network analysis (overlap of vertices not in the midline and those included in the yeo networks).
 - kfold_fc_r: subjectwise correlation between empirical and predicted functional connectivity in the discovery dataset.
 - microstructural_features: curvature, cortical thickness, and t1w/t2w intensities
 - mics_fc_r: subjectwise correlation between empirical and predicted functional connectivity in the MICS dataset.
 - node_strength: node strength of the temporal lobe
 - r: vertexwise correlation between predicted and empirical data in the discovery dataset
 - r_ho: vertexwise correlation between predicted and empirical data in the replication and MICS datasets
 - repl_fc_r subjetwise correlation between empirical and predicted functional connectivity in the replication dataset.
 - sc_mask: log-transformed (for visualization only!) structural connectivity of the discovery dataset.
 - sjh: parcellation used for the MPC gradient
 - surf_lh: left hemispheric surface
 - surf_rh: right hemispheric surface
 - temporalLobe_msk: temporal lobe mask
 - yeo: Yeo networks
 - yeo_tl: Yeo networks in the temporal lobe.
 - yeo_predicted: Predicted yeo networks in the discovery dataset of one of the folds.

License
===========
The data and code herein are published under a `BSD-3 license <https://github.com/MICA-MNI/micaopen/blob/master/temporal_gradients/LICENSE>`_. Please note that this license only applies to the :matlab:`temporal_gradients` sub-directory of :matlab:`micaopen` and overrides the license in the root directory. 

If you use any of the code or data in this package, then please consider citing `Vos de Wael et al., 2020, bioRxiv <https://www.biorxiv.org/content/10.1101/2020.11.26.400382v1>`_.
