# BACion

## Prediction of the Maximum NaCl Concentration Supporting Bacterial Growth

BACion is a proteome-based machine-learning tool designed to predict the **maximum NaCl concentration supporting bacterial growth**.

The model accepts a bacterial protein FASTA file as input and uses proteome-derived features with an XGBoost regression model to estimate the **maximum NaCl concentration that can support bacterial growth**.

## Features

* Protein FASTA input
* Whole-proteome feature extraction
* XGBoost-based prediction
* Prediction of maximum NaCl concentration supporting bacterial growth
* Reproducible Python package
* Google Colab workflow
* Example proteome included
* Model and feature configuration distributed with the repository

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
```
