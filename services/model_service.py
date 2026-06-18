"""Chargement du modèle et logique de prédiction."""

from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd

from config.settings import DEFAULT_MAP_CENTER, METADATA_PATH, MODEL_PATH, QUARTIER_COORDS


class LoyerModelService:
    """Interface entre l'application Streamlit et le modèle .joblib."""

    def __init__(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Modèle introuvable : {MODEL_PATH}\n\n"
                "Étapes :\n"
                "  1) Ouvrir TP_Regression_lineaire.ipynb\n"
                "  2) Exécuter toutes les cellules jusqu'à la sauvegarde\n"
                "  3) Vérifier que models/modele_loyer.joblib existe"
            )
        self.model = joblib.load(MODEL_PATH)
        with open(METADATA_PATH, encoding="utf-8") as f:
            self.metadata = json.load(f)
        self.feature_columns = self.metadata["feature_columns"]

    def build_features(self, inputs: dict) -> pd.DataFrame:
        """Transforme les champs du formulaire en DataFrame pour le modèle."""
        row = {
            "superficie": inputs["superficie"],
            "nombre_chambres": inputs["nombre_chambres"],
            "douche_wc": 1 if inputs["douche_wc"] == "interieur" else 0,
            "meuble": 1 if inputs["meuble"] == "oui" else 0,
            "etat_general": {"mauvais": 0, "moyen": 1, "bon": 2}[inputs["etat_general"]],
            "superficie_par_chambre": inputs["superficie"] / inputs["nombre_chambres"],
            "superficie_sqrt": float(np.sqrt(inputs["superficie"])),
        }

        for quartier in self.metadata["quartiers"]:
            col = f"quartier_{quartier}"
            if col in self.feature_columns:
                row[col] = 1 if inputs["quartier"] == quartier else 0

        for type_acces in self.metadata["types_acces"]:
            col = f"type_d_acces_{type_acces}"
            if col in self.feature_columns:
                row[col] = 1 if inputs["type_d_acces"] == type_acces else 0

        return pd.DataFrame([row])[self.feature_columns]

    def predict(self, inputs: dict) -> float:
        prediction = float(self.model.predict(self.build_features(inputs))[0])
        return max(prediction, 0.0)

    def get_feature_weights(self, top_n: int = 12) -> pd.DataFrame:
        preprocessor = self.model.named_steps["preprocessor"]
        regressor = self.model.named_steps["regressor"]
        names = preprocessor.get_feature_names_out()
        coefs = regressor.coef_

        weights = pd.DataFrame(
            {"variable": names, "poids": coefs, "importance": np.abs(coefs)}
        ).sort_values("importance", ascending=False)

        return weights.head(top_n).sort_values("poids")

    @staticmethod
    def get_quartier_coords(quartier: str) -> tuple[float, float]:
        return QUARTIER_COORDS.get(quartier, DEFAULT_MAP_CENTER)
