# BACion — How to Run

## Predicting the Maximum NaCl Concentration Supporting Bacterial Growth

BACion is a proteome-based machine-learning tool that predicts the **maximum NaCl concentration supporting bacterial growth** from a bacterial protein FASTA proteome.

# Google Colab

This is the **recommended method for most users**.

No local Python installation is required.

## Step 1 — Open BACion in Google Colab

Click the button below:

[![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bisalzindal-blip/Prediction-of-the-Maximum-NaCl-Concentration-Supporting-Bacterial-Growth/blob/main/BACion/notebooks/BACion_Colab.ipynb)

## Step 2 — Run the BACion cell

The Colab notebook contains a single executable code cell.

Click the ▶ Run button.

BACion will automatically:

1. Clone the BACion repository
2. Install the required dependencies
3. Install the BACion package
4. Load the trained XGBoost model
5. Ask for a bacterial protein FASTA file
6. Validate the FASTA file
7. Extract the required features
8. Predict the **maximum NaCl concentration supporting bacterial growth**
9. Display the prediction
10. Generate a TXT report

## Step 3 — Upload a bacterial protein FASTA file

When Colab asks for an input file, upload a bacterial protein proteome.

Supported formats:

* `.faa`
* `.fa`
* `.fasta`

### Recommended input

A complete bacterial protein proteome generated from a bacterial genome.

Example:

```text
proteome.faa
```

BACion analyzes the complete bacterial protein proteome and uses the extracted proteome-level features to predict the **maximum NaCl concentration that can support bacterial growth**.
