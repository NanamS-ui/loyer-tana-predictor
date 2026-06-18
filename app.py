"""
Point d'entrée Streamlit — Partie 4 du TP Régression Linéaire.

Structure du projet :
  app.py              → lance l'interface
  config/             → chemins et constantes
  services/           → chargement du modèle + prédiction
  ui/                 → composants visuels (formulaire, résultats, carte)
  models/             → modèle exporté localement depuis le notebook (non versionné)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Permet les imports config/, services/, ui/
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from services import LoyerModelService
from ui import render_map, render_results, render_sidebar

st.set_page_config(
    page_title="Prédiction loyer — Antananarivo",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Prédiction du loyer mensuel à Antananarivo")
st.markdown(
    "Application Streamlit alimentée par le modèle entraîné dans le notebook TP."
)

try:
    service = LoyerModelService()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()

with st.sidebar:
    inputs, predict_clicked = render_sidebar(service.metadata)

loyer = service.predict(inputs) if predict_clicked else None

col_resultats, col_carte = st.columns([1, 1])

with col_resultats:
    render_results(service, inputs, predict_clicked, loyer)

with col_carte:
    render_map(service, inputs["quartier"], loyer if predict_clicked else None)

st.divider()
st.caption("TP Régression Linéaire — Partie 4 | Modèle : Polynomial + Ridge")
