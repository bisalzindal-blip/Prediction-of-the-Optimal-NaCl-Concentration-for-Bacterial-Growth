"""
BACion prediction module.

Loads the trained XGBoost model and predicts the optimal NaCl
concentration for bacterial growth from a bacterial proteome FASTA.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd
import xgboost as xgb

from .features import align_features, extract_features


class BACionPredictor:
    """
    BACion XGBoost predictor.

    Parameters
    ----------
    model_path : str or Path
        Path to bacion_xgboost.json.

    feature_config_path : str or Path
        Path to feature_config.json.

    feature_names_path : str or Path
        Path to feature_names.json.
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        feature_config_path: Union[str, Path],
        feature_names_path: Union[str, Path],
    ) -> None:

        self.model_path = Path(model_path)
        self.feature_config_path = Path(
            feature_config_path
        )
        self.feature_names_path = Path(
            feature_names_path
        )

        self._check_files()


        # Load feature configuration

        with open(
            self.feature_config_path,
            "r",
            encoding="utf-8",
        ) as handle:

            self.feature_config = json.load(handle)

   
        # Load feature names
        with open(
            self.feature_names_path,
            "r",
            encoding="utf-8",
        ) as handle:

            self.feature_names = json.load(handle)

        if isinstance(self.feature_names, dict):

            # Support common JSON formats
            if "feature_names" in self.feature_names:
                self.feature_names = (
                    self.feature_names["feature_names"]
                )

            elif "features" in self.feature_names:
                self.feature_names = (
                    self.feature_names["features"]
                )

        if not isinstance(
            self.feature_names,
            list,
        ):

            raise ValueError(
                "feature_names.json must contain a list "
                "of feature names."
            )

        # Load XGBoost model

        self.model = xgb.XGBRegressor()

        self.model.load_model(
            str(self.model_path)
        )

    def _check_files(self) -> None:
        """Check that all required model files exist."""

        required = [
            self.model_path,
            self.feature_config_path,
            self.feature_names_path,
        ]

        missing = [
            str(path)
            for path in required
            if not path.exists()
        ]

        if missing:

            raise FileNotFoundError(
                "Missing BACion model files:\n"
                + "\n".join(missing)
            )

    def calculate_features(
        self,
        fasta_path: Union[str, Path],
    ) -> pd.DataFrame:
        """
        Calculate and align features for a proteome.

        Parameters
        ----------
        fasta_path : str or Path
            Protein FASTA file.

        Returns
        -------
        pandas.DataFrame
            Model-ready feature matrix.
        """

        features = extract_features(
            fasta_path
        )

        aligned = align_features(
            features,
            self.feature_names,
        )

        return aligned

    def predict_value(
        self,
        fasta_path: Union[str, Path],
    ) -> float:
        """
        Predict the optimal NaCl concentration.

        Parameters
        ----------
        fasta_path : str or Path
            Protein FASTA file.

        Returns
        -------
        float
            Predicted NaCl concentration.
        """

        X = self.calculate_features(
            fasta_path
        )

        prediction = self.model.predict(X)

        return float(
            np.asarray(prediction).reshape(-1)[0]
        )

    def predict(
        self,
        fasta_path: Union[str, Path],
    ) -> Dict[str, Any]:
        """
        Predict optimal NaCl concentration and return
        a structured result.

        Parameters
        ----------
        fasta_path : str or Path
            Protein FASTA file.

        Returns
        -------
        dict
            Prediction result.
        """

        fasta_path = Path(fasta_path)

        X = self.calculate_features(
            fasta_path
        )

        prediction = self.model.predict(X)

        predicted_nacl = float(
            np.asarray(prediction).reshape(-1)[0]
        )

        result = {
            "model": "BACion",
            "model_version": "1.0.0",
            "input_file": fasta_path.name,
            "protein_count": None,
            "predicted_optimal_NaCl_percent": predicted_nacl,
            "feature_count": int(X.shape[1]),
        }

        # Try to obtain protein count directly
        try:

            from .features import read_proteome

            sequences = read_proteome(
                fasta_path
            )

            result["protein_count"] = len(
                sequences
            )

        except Exception:
            pass

        return result
