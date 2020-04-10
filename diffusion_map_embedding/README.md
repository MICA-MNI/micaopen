### Diffusion map embedding MATLAB code
To run diffusion embedding: let `z` be your z-scored connectivity matrix. 
```
N = connectivity2normangle(z)
[emb,res] = mica_diffusionEmbedding(N); 
```
Alternatively, one can use name-value pairs in the `mica_diffusionEmbedding` function. Run `help mica_diffusionEmbedding` in MATLAB for details. 

To align sets of gradients, use `mica_iterativeAlignment` as follows. Let `C` be a cell array where each cell contains an `emb` from a separate datset. 
```
nIterations = 100
[realigned,xfms] = mica_iterativeAlignment(C,nIterations)
```
Normally, `mica_iterativeAlignment` initiates by aligning to the first embedding in `C`. To specify a different first target, supply the first target as a third argument. 

Note: The gradient identification and analysis workflopw has now been integrated into the BrainSpace toolbox. Please consider using https://github.com/MICA-MNI/BrainSpace instead, as it gives more flexible data handling, additional functions, and python/matlab support. More information on BrainSpace is provided at http://readthedocs.brainspace.io and the associated paper "BrainSpace: a toolbox for the analysis of macroscale gradients in neuroimaging and connectomics datasets" by Vos de Wael et al. can be found here https://www.nature.com/articles/s42003-020-0794-7


