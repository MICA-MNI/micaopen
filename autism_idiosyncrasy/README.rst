Connectivity alterations in autism reflect functional idiosyncrasy
------------------------------------------------------------------

.. image:: https://img.shields.io/badge/Made%20with-Python-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

|

This repo contains code for our work on functional idiosyncrasy in autism.

Manuscript
~~~~~~~~~~
Benkarim O, Paquola C, Park B, Hong SJ, Royer J, Vos de Wael R, Lariviere S, Valk S, Bzdok D, Mottron L,
Bernhardt B. (2021) *Connectivity alterations in autism reflect functional idiosyncrasy*. Under review


Code
~~~~
These are the main functions to run the analysis:

.. code-block:: python

    from embedding import generate_embeddings, compute_sd, compute_dd

    # Generate embedding and ICN clustering
    res = generate_embeddings(...)

    # Idiosyncrasy descriptors
    SD = compute_sd(...)  # Surface distance
    DD = compute_dd(...)  # Diffusion distance


    from overlap import analyze_entropy, analyze_overlap

    # Analyze ICSs entropy in TD vs ASD
    df_ent, delta_ent = analyze_entropy(...)

    # Analyze ICNs overlap in TD vs ASD
    df_overlap, df_ols, df_icn_size = analyze_overlap(...)


    from ados import analyze_ados

    # Association of idiosyncrasy with ADOS CSS
    df_ados = analyze_ados(...)


    from gene_enrich import select_genes

    # Gene enrichment analysis
    selected_genes, df_genes = select_genes(...)


    from connectivity import analyze_connectivity

    # Analysis of connectivity (DC: degree centrality and EC: eigenvector
    # centrality) alterations before and after accounting for
    # idiosyncrasy (i.e., hat)
    dc_sig, dc_hat_sig, ec_sig, ec_hat_sig = analyze_connectivity(...)





Dependencies
~~~~~~~~~~~~
* `numpy <https://numpy.org/>`_
* `scipy <https://scipy.org/scipylib/index.html>`_
* `pandas <https://nipy.org/nibabel/index.html>`_
* `scikit-learn <https://scikit-learn.org/stable/>`_
* `statsmodels <https://nilearn.github.io/>`_
* `brainspace <https://brainspace.readthedocs.io/en/latest/index.html>`_
* `mne <https://mne.tools/0.15/index.html>`_


The code was tested in Python 3.6-3.8.

License
~~~~~~~

The source code is available under the `BSD (3-Clause) license <https://github.com/OualidBenkarim/ps_diversity/blob/main/LICENSE>`_.