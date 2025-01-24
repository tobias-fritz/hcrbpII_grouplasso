# Spectral Tuning in Human Cellular Retinol Binding Protein II (hCRBPII)

## Introduction

Human cellular retinol-binding protein II (CRBP II) is an excellent model system for studying absorption shifts in retinol chromophores. Its structure is well characterized, and its binding site is located deep within the protein core, providing a unique environment for studying the effects of substitutions on the chromophore. Polarization and electrostatic effects can stabilize the ground or excited state energy levels of the retinal chromophore, perturbing the Schiff-base or β-ionone moieties and influencing charge transfer within the molecule, leading to shifts in measured absorption spectra [1][2].

Several studies have explored the absorption-shifting effects of different substitutions both experimentally and in silico [1][2]. In this notebook, I briefly introduce how we can analyze the mutation data obtained from these studies to identify and quantify the effects of these substitutions on the absorption properties of the chromophore in hCRBP II. This approach is based on Karasuyama, M. et al. using an ML group-wise sparsity regularization approach to identify color-tuning rules in Rhodopsins [3]. Sparse group lasso regularizers are a type of regularization technique used in machine learning to identify important features and reduce overfitting. They work by promoting sparsity both within individual feature groups and across all feature groups simultaneously, allowing for the selection of a subset of the most relevant features. By analyzing the coefficients of the model, we can gain insights into the effects of different substitutions on the absorption properties of the chromophore without prior knowledge of the protein structure.

For more information about the theory of group lasso regularization, read the documentation that can be found [here](https://group-lasso.readthedocs.io/en/latest/index.html).

## Running the Notebook

You can run the notebook online using Binder. Click the badge below to launch the notebook:

 [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tobias-fritz/hcrbpII_grouplasso/HEAD)
 
## How to use

- You can also run the model from ```hcrbpII.ipynb``` localy, after installing the dependencies from the ```enviornment.yml``` using conda with: ```conda env create -f environment.yml```
- In the notebook, a precompiled ```gl``` model is loaded from the data folder, compiled with gamma=0.11, n_iter=15000, tol=1e-8
- Please make sure to use the proper citations when using the data, sourced from scientifc work (in this casse  Wenjing Wang et al. Science 338,1340-1343 (2012). DOI:10.1126/science.1226135). 
- In data/hcrbpII.csv, references are provided for each data entry used in this notebook.

## How to Use
- Try it out online by clicking on the Binder badge here &rarr; [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tobias-fritz/hcrbpII_grouplasso/HEAD)
- You can also run the model from `hcrbpII.ipynb` locally, after installing the dependencies from the `environment.yml` using conda with: `conda env create -f environment.yml`
- In the notebook, a precompiled `gl` model is loaded from the data folder, compiled with gamma=0.11, n_iter=15000, tol=1e-8
- Please make sure to use the proper citations when using the data, sourced from scientific work (in this case Wenjing Wang et al. Science 338, 1340-1343 (2012). DOI:10.1126/science.1226135).
- In `data/hcrbpII.csv`, references are provided for each data entry used in this notebook.

## References
[1]: C.-M. Suomivuori, L. Lang, D. Sundholm, A. P. Gamiz-Hernandez, V. R. I. Kaila, Chem. Eur. J. 2016, 22, 8254
[2]: Wenjing Wang et al. Science 338, 1340-1343 (2012). DOI:10.1126/science.1226135
[3]: Karasuyama, M., Inoue, K., Nakamura, R. et al. Sci Rep 8, 15580 (2018)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
