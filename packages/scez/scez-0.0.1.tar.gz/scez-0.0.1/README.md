## scez – single cell, easy mode
[![package](https://github.com/abearab/scez/actions/workflows/main.yml/badge.svg)](https://github.com/abearab/scez/actions/workflows/main.yml)

### Installation
Make sure you have mamba installed in your base environment. If not, install it with:
```bash
conda install mamba -n base -c conda-forge
```
Then, create a new conda environment with the provided `environment.yml` file and activate it. This will install all necessary dependencies for scez.
```bash
conda env create -f environment.yml

conda activate scez
```
Finally, install scez with:

```bash
pip install scez
```

Or, if you want to install the latest version from the repository:
```bash
pip install git+https://github.com/abearab/scez.git
```
