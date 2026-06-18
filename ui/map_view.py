"""Carte interactive du quartier sélectionné."""

from __future__ import annotations

import folium
import streamlit as st
from streamlit_folium import st_folium

from services.model_service import LoyerModelService


def render_map(
    service: LoyerModelService,
    quartier: str,
    loyer: float | None,
) -> None:
    st.subheader("Localisation du quartier")
    lat, lon = service.get_quartier_coords(quartier)

    carte = folium.Map(location=[lat, lon], zoom_start=14, tiles="OpenStreetMap")
    folium.Marker(
        [lat, lon],
        popup=quartier,
        tooltip=f"Quartier : {quartier}",
        icon=folium.Icon(color="blue", icon="home", prefix="fa"),
    ).add_to(carte)

    if loyer is not None:
        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            popup=f"Loyer estimé : {loyer:,.0f} Ar",
            color="#27ae60",
            fill=True,
            fill_color="#2ecc71",
        ).add_to(carte)

    st_folium(carte, width=None, height=450, returned_objects=[])
