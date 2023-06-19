A Riemannian approach to predicting brain function from the structural connectome
---------------------------------------------------------------------------------

.. image:: https://img.shields.io/badge/Made%20with-Python-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

|

This repo contains code for our work on the prediction of brain function from the structural connectome using diffusion maps and Riemannian optimization

Manuscript
~~~~~~~~~~
Benkarim O, Paquola C, Park B, Royer J, Rodríguez-Cruces R, Vos de Wael R, Misic B, Piella G, Bernhardt B. (2022) *A Riemannian approach to predicting brain function from the structural
connectome*. NeuroImage 257, 119299. https://doi.org/10.1016/j.neuroimage.2022.119299.


Code
~~~~
This is the main function to test our method:

.. code-block:: python

    from utils import run_sf_prediction

    scores, params, preds = run_sf_prediction(sc_train, fc_train, ...)


Dependencies
~~~~~~~~~~~~
* `numpy <https://numpy.org/>`_
* `scipy <https://scipy.org/scipylib/index.html>`_
* `pandas <https://nipy.org/nibabel/index.html>`_
* `scikit-learn <https://scikit-learn.org/stable/>`_
* `brainspace <https://brainspace.readthedocs.io/en/latest/index.html>`_
* `pymanopt=0.2.5 <https://www.pymanopt.org/>`_


The code was tested in Python 3.7-3.9.

License
~~~~~~~

The source code is available under the `BSD (3-Clause) license <https://github.com/OualidBenkarim/ps_diversity/blob/main/LICENSE>`_.