
# Structural Manifold
> Data and code to use the structural manifold as a standard space or create your own  <br /> 
> From "The Cortical Wiring Scheme of Hierarchical Information Processing", Paquola et al., 2020  <br />
> https://www.biorxiv.org/content/10.1101/2020.01.08.899583v1 <br />

![](https://github.com/MICA-MNI/micaopen/blob/master/structural_manifold/method_overview.png)

---

## Table of Contents

- [Standard space](#standard-space)
- [Step by step guide to building the structural manifold](#step-by-step)
- [Manuscript data](#manuscript-data) 
- [Feature notes](#feature-notes)
- [Support](#support)

---

### Standard space

- The first two columns of 'eigenvectors.csv' represent the x and y dimensions of the structural manifold and the rows are parcels. We can reveal  pattens in data by projecting the values into this space. For example, using scatter(eigenvector(:,1), eigenvector(:,2),10, data) in matlab. 
- The dominant axis of variation of any data projected into the space can be approximated by correlating the data with the superimposed axes, which are contained in 'noncardinal_axes.csv'. This can be performed with complete data or data in only a few nodes, thus allowing for extrapolation for spatially sparse data to large-scale anatomical gradients.
- 'md_group.csv' contains the manifold distance between each pair of nodes and can be used as a simple measure of cortico-cortical wiring. 


### Step by step

Build your own structural manifold with the following steps. <br /> 
This tutorial can be followed using the group-level metadata. 

1. Normalisation: We peformed rank normalisation and rescaling to enforce the same range of values for each modality, accounting for the variations in sparsity. This helps to equalise the contribution of each modality, without enforcing an arbitary threshold. 

```matlab
    % add paths to necessary scripts
    micaRepo = '/path/to/micaopen/';
    addpath([micaRepo '/diffusion_map_embedding']);
    addpath([micaRepo '/structural_manifold']);

    % tract strength
    [~, idx]  = sort(ts_group(:), 'ascend');   % larger numbers are higher rank
    ts_norm   = sort_back((1:length(ts_group(:)))', idx);
    ts_norm   = reshape(ts_norm, [size(ts_group)]);
    ts_norm   = (ts_norm - (numel(ts_group) - nnz(ts_group))) .* (ts_group>0);
    
    % geodesic distance
    this_gd     = 1./gd_group;  % invert distance matrix
    [~, idx]    = sort(this_gd(:), 'ascend');
    this_gd     = sort_back((1:length(this_gd(:)))', idx);
    this_gd(this_gd==0) = nan;
    gd_scale   = rescale(this_gd(:), 1, max(ts_norm(:)));
    gd_norm    = reshape(gd_scale, [size(gd_group)]);
    gd_norm(isnan(gd_norm)) = 0;
    
    % microstructure profile covariance
    [~, idx] = sort(mpc_group(:), 'ascend');  % larger numbers are higher rank
    this_mpc = sort_back((1:length(mpc_group(:)))', idx);
    this_mpc = rescale(this_mpc(:), 1, max(ts_norm(:)));
    this_mpc(this_mpc==0) = nan;
    mpc_scale  = rescale(this_mpc(:), 1, max(ts_norm(:)));
    mpc_norm   = reshape(mpc_scale, [size(mpc_group)]);
    mpc_norm(isnan(mpc_norm)) = 0;
```

2. Fusion: Horizontal concatenation of matrices and production of a node-to-node affinity matrix using row-wise normalised angle similarity

```matlab
  mat_horz            = [gd_norm mpc_norm cs_norm];
  affinity_matrix     = 1-squareform(pdist(mat_horz'.','cosine'));
  affinity_matrix(isnan(affinity_matrix)) = 0;
  norm_angle_matrix    = 1-acos(affinity_matrix)/pi;
```
3. Manifold learning: Diffusion map embedding was employed to gain a low dimensional representation of cortical wiring. The decay of an eigenvector provides an integrative measure of the connectivity between nodes along a certain axis. This lower dimensional representation of cortical wiring is especially interesting for interrogating the cortical hierarchy, which previous research suggests extends upon sensory-fugal and anterior-posterior axes. 
  
```matlab
  [eigenvectors, results] = mica_diffusioneigenvectors(norm_angle_matrix, 'symmetryMargin', 1e-05);
  eigenvectors(:,2) = eigenvectors(:,2).*-1; % the signs of the eigenvectors are arbitrary, so we flip the second for interpretability
  colour_coding = colour2gradients(eigenvectors(:,2), eigenvectors(:,1));
```

### Manuscript data

- Data corresponding to the Figures and Supplementary Figures presented in the manuscript can be found in the Manuscript_Data.xlsx. 
- Instructions of how to interpret Manuscript_Data.xlsx, linking Figures to the columns and sheets, can be found in Manuscript_Data_Dictionary.docx


### Feature notes

- The parcellation is provided on fsavearage (.annot) and conte69 (.csv) <br /> 
- The first label in each hemisphere of the annotation file and the '0' in the csv file comprise the medial wall and are not used in the analysis

---

### Support

Feel free to get in touch if you have any questions (casey.paquola@mail.mcgill.ca)
