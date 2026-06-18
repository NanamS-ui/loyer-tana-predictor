"""Affichage de la prédiction et des coefficients du modèle."""

from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from services.model_service import LoyerModelService


def render_results(
    service: LoyerModelService,
    inputs: dict,
    predict_clicked: bool,
    loyer: float | None,
) -> None:
    st.subheader("Résultat de la prédiction")

    if predict_clicked and loyer is not None:
        st.success(f"**Loyer estimé : {loyer:,.0f} Ar / mois**")
        st.caption(f"Soit environ **{loyer / inputs['superficie']:,.0f} Ar/m²**")
    else:
        st.info("Renseignez le formulaire à gauche, puis cliquez sur **Prédire le loyer**.")

    st.subheader("Poids des variables du modèle")
    weights = service.get_feature_weights()

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#2ecc71" if p > 0 else "#e74c3c" for p in weights["poids"]]
    ax.barh(weights["variable"], weights["poids"], color=colors)
    ax.set_xlabel("Coefficient (après transformation polynomiale)")
    ax.set_title("Influence des variables sur le loyer")
    ax.invert_yaxis()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Voir le tableau des coefficients"):
        st.dataframe(
            weights.rename(columns={"variable": "Variable", "poids": "Poids"}),
            use_container_width=True,
            hide_index=True,
        )
