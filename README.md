# BACion

## Prediction of the Optimal NaCl Concentration for Bacterial Growth

BACion is a proteome-based machine-learning tool designed to predict the optimal NaCl concentration associated with bacterial growth.

The model accepts a bacterial protein FASTA file as input and uses proteome-derived features with an XGBoost regression model to estimate the optimal NaCl concentration.


## Features

- Protein FASTA input
- Whole-proteome feature extraction
- XGBoost-based prediction
- Reproducible Python package
- Google Colab workflow
- Example proteome included
- Model and feature configuration distributed with the repository

## Citation
If you use Bacion in your research, please cite:
Zindal, B. (2026). Bacion: Prediction of the Optimal NaCl Concentration for Bacterial Growth (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.22069575

## Repository structure

```text
BACion/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── model/
│   ├── bacion_xgboost.json
│   ├── feature_config.json
│   └── feature_names.json
│
├── src/
│   └── bacion/
│       ├── __init__.py
│       ├── features.py
│       └── predictor.py
│
├── notebooks/
│   └── BACion_Colab.ipynb
│
└── examples/
    └── example_proteome.faa
