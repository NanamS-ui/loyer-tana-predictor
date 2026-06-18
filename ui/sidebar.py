"""Formulaire de saisie (barre latérale Streamlit)."""

from __future__ import annotations

import streamlit as st


def render_sidebar(metadata: dict) -> tuple[dict, bool]:
    """Affiche le formulaire et retourne (données saisies, bouton cliqué)."""
    st.header("Caractéristiques du logement")

    inputs = {
        "quartier": st.selectbox("Quartier", metadata["quartiers"]),
        "superficie": st.number_input("Superficie (m²)", min_value=15, max_value=300, value=80),
        "nombre_chambres": st.number_input("Nombre de chambres", min_value=1, max_value=10, value=3),
        "douche_wc": st.selectbox("Douche / WC", ["interieur", "exterieur"]),
        "type_d_acces": st.selectbox("Type d'accès", metadata["types_acces"]),
        "meuble": st.selectbox("Meublé", ["non", "oui"]),
        "etat_general": st.selectbox("État général", ["mauvais", "moyen", "bon"]),
    }

    predict_clicked = st.button("Prédire le loyer", type="primary", use_container_width=True)
    return inputs, predict_clicked
