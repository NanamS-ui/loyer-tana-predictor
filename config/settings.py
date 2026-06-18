"""Chemins et constantes du projet."""

from pathlib import Path

# Racine du projet Streamlit
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dossier des modèles exportés depuis le notebook
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "modele_loyer.joblib"
METADATA_PATH = MODELS_DIR / "metadata.json"

# Dataset du TP (utilisé uniquement par scripts/train_and_export.py)
DATASET_PATH = PROJECT_ROOT.parent / "Régression Linéaire" / "dataset_location_madagascar.csv"

# Coordonnées approximatives des quartiers (carte Folium)
QUARTIER_COORDS = {
    "67 Ha": (-18.8700, 47.5300),
    "Ambatobe": (-18.8890, 47.5580),
    "Ambohibao": (-18.8420, 47.4780),
    "Ambohimanarina": (-18.9050, 47.5480),
    "Ampefiloha": (-18.9050, 47.5180),
    "Analakely": (-18.9137, 47.5219),
    "Andraharo": (-18.8980, 47.5350),
    "Ankorondrano": (-18.8760, 47.5080),
    "Anosibe": (-18.9200, 47.5350),
    "Antanimena": (-18.9100, 47.5280),
    "Isoraka": (-18.9100, 47.5250),
    "Itaosy": (-18.9200, 47.4920),
    "Ivandry": (-18.8670, 47.4760),
    "Mahamasina": (-18.9150, 47.5350),
}

DEFAULT_MAP_CENTER = (-18.8792, 47.5079)
