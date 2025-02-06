#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.io as pio

# Charger les données depuis GitHub
data_path = "https://raw.githubusercontent.com/tolletg/Dash_Cabouy/main/Cabouy_Interpolated.xlsx"
data = pd.read_excel(data_path)

# Nettoyage des noms de colonnes
data.columns = [col.strip().replace(" ", "_") for col in data.columns]

# Exclure DATE et Conductivité_Moyenne_Mobile
excluded_columns = ["DATE", "Conductivité_Moyenne_Mobile"]
parametres = [col for col in data.columns if col not in excluded_columns and not col.startswith("Statut_")]

# Créer l'application Dash
app = dash.Dash(__name__)

# Mise en page de l'application
app.layout = html.Div([
    html.H1("Visualisation des Données Hydrologiques de la station de Cabouy "),
    dcc.Dropdown(
        id="param-dropdown",
        options=[{"label": param, "value": param} for param in parametres],
        value="Niveau_(cm)"  # Valeur par défaut
    ),
    dcc.Graph(id="graph"),
    html.Div(id="error-message", style={"color": "red", "font-weight": "bold"})
])

# Callback pour mettre à jour le graphique
@app.callback(
    [dash.dependencies.Output("graph", "figure"),
     dash.dependencies.Output("error-message", "children")],
    [dash.dependencies.Input("param-dropdown", "value")]
)
def update_graph(param):
    if param not in data.columns:
        return {"data": [], "layout": {"title": f"❌ Erreur : {param} non trouvé"}}, f"⚠️ Erreur : {param} non trouvé."

    # Ajouter une colonne de statut (si elle existe dans les données)
    statut_col = "Statut_" + param if "Statut_" + param in data.columns else None

    # Convertir en numérique
    data[param] = pd.to_numeric(data[param], errors='coerce')

    # Création du graphique interactif
    fig = px.scatter(
        data,
        x="DATE",
        y=param,
        color=statut_col,  # Utiliser la colonne statut
        title=f"Evolution du paramètre : {param}",
        labels={param: param, "DATE": "Date"},
    )

    # Ajustement dynamique de l'axe Y
    fig.update_layout(yaxis=dict(range=[data[param].min(), data[param].max()]))

    # Retourner le graphique et le message d'erreur
    return fig, ""

# Définir l'instance du serveur
server = app.server


# In[3]:





# In[ ]:




