#!/usr/bin/env python
# coding: utf-8

# In[3]:


import logging
import pandas as pd
import os
import dash
from dash import dcc, html
import plotly.express as px

GITHUB_URL = "https://github.com/tolletg/Dash_Cabouy/raw/refs/heads/main/Data/"

STATIONS = {
    "Alzou": "Alzou.xlsx",
    "Cabouy": "Cabouy.xlsx",
    "Combettes": "Combettes.xlsx",
    "Fonbelle": "Fonbelle.xlsx",
    "Goudou": "Goudou.xlsx",
    "Méduse": "Meduse.xlsx",
    "OuysseCales": "OuysseCales.xlsx",
    "Plana_Lac": "Plana_Lac.xlsx",
    "Plana_Riviere": "Plana_Riviere.xlsx",
    "St_Sauveur": "St_Sauveur.xlsx",
    "Thémines": "Themines.xlsx",
    "Théminettes": "Theminettes.xlsx",
    "Zobépine": "Zobepine.xlsx"
}

data_cache = {}

logging.basicConfig(level=logging.INFO)

for station, filename in STATIONS.items():
    url = GITHUB_URL + filename
    try:
        logging.info(f" Chargement de {station} depuis {url}")
        
        if filename.endswith(".xlsx"):
            df = pd.read_excel(url, engine="openpyxl")
        else:
            df = pd.read_csv(url, encoding="utf-8", sep=";", decimal=",")

        df.columns = [col.strip().replace(" ", "_") for col in df.columns]

        if "DATE" in df.columns:
            df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce") 

        df = df.sort_values("DATE")

        data_cache[station] = df

    except Exception as e:
        logging.error(f"Erreur lors du chargement de {station} : {str(e)}")
        data_cache[station] = None

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Visualisation des données hydrologiques de l'Ouysse - Parc Naturel des Causses du Quercy"),
    
    # Titre pour la sélection de la station
    html.H3("Station"),
    
    # Sélection de la station (fichier)
    dcc.Dropdown(
        id="station-dropdown",
        options=[{"label": name, "value": name} for name in STATIONS.keys()],
        value=list(STATIONS.keys())[0] if STATIONS else None,  # Première station par défaut
        placeholder="Sélectionnez une station",
    ),
    
    # Titre pour la sélection du paramètre
    html.H3("Paramètre"),
    
    # Sélection du paramètre
    dcc.Dropdown(
        id="param-dropdown",
        placeholder="Sélectionnez un paramètre"
    ),
    
    dcc.Graph(id="graph"),
    
    html.Div(id="error-message", style={"color": "red", "font-weight": "bold"})
])

@app.callback(
    [dash.dependencies.Output("param-dropdown", "options"),
     dash.dependencies.Output("param-dropdown", "value")],
    [dash.dependencies.Input("station-dropdown", "value")]
)
def update_param_options(station):
    if not station or station not in data_cache or data_cache[station] is None:
        return [], None

    df = data_cache[station]

    # Exclure DATE et colonnes de statut
    excluded_columns = ["DATE"]
    parametres = [col for col in df.columns if col not in excluded_columns and not col.startswith("Statut_")]

    return [{"label": param, "value": param} for param in parametres], parametres[0] if parametres else None

@app.callback(
    [dash.dependencies.Output("graph", "figure"),
     dash.dependencies.Output("error-message", "children")],
    [dash.dependencies.Input("station-dropdown", "value"),
     dash.dependencies.Input("param-dropdown", "value")]
)
def update_graph(station, param):
    if not station or station not in data_cache or data_cache[station] is None:
        return {"data": [], "layout": {"title": "Aucune donnée"}}, "⚠️ Veuillez sélectionner une station."

    df = data_cache[station]

    if param not in df.columns:
        return {"data": [], "layout": {"title": f"❌ Erreur : {param} non trouvé"}}, f"⚠️ Erreur : {param} non trouvé."

    # Gestion des statuts
    statut_col = "Statut_" + param if "Statut_" + param in df.columns else None

    # Convertir en numérique
    df[param] = pd.to_numeric(df[param], errors='coerce')

    # Création du graphique
    fig = px.scatter(
        df,
        x="DATE",
        y=param,
        color=statut_col,
        title=f"{param} ({station})",
        labels={param: param, "DATE": "Date"},
    )

    fig.update_layout(yaxis=dict(range=[df[param].min(), df[param].max()]))

    return fig, ""

server = app.server

port = int(os.getenv('PORT', 8050))

if __name__ == "__main__":
    app.run_server(debug=True, port=port)


# In[ ]:




