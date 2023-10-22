import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import ast
from dash.dependencies import Input, Output
import plotly.graph_objs as go


st.title ('🇫🇷Consommation énergetique en France 2011-2021')
st.title('Comment la consommation d\'électricité et de gaz en France a-t-elle évolué au cours de la dernière décennie ?')

# Création d'un menu
st.sidebar.title('Menu')
st.sidebar.markdown("""
- [Descreption du projet](#project-description-)
- [Evolution de la consommation 2011 à 2021](#Evolution-de-la-consommation-2011-à-2021)
- [Les 5 plus grands secteurs de la consommation](#Les-5-plus-grands-secteurs-de-la-consommation)
- [Les 5 principaux opérateurs de consommation ](#Les-5-principaux-opérateurs-de-consommation)
- [Comparaison évolution en France et en UE ](#Comparaison-évolution-en-France-et-en-UE)
- [Évolutionde stockage de Gaz en France](#Évolution-de-stockage-de-Gaz-en-France)

""")
st.sidebar.markdown('<p style="color: red ; font-size: 30px; font-weight: bold; display : inline"> #datavz2023efrei </p>', unsafe_allow_html=True)
st.sidebar.write('Alina Hodovanska BIA1')

# Add an anchor tag for the section
st.markdown('<a id="project-description-"></a>', unsafe_allow_html=True)
st.header('Descreption du projet')

st.write("""
    Ce projet analyse la consommation d'électricité et de gaz en France sur une décennie, de 2011 à 2021. Il se penche sur les tendances annuelles, les principaux secteurs d'utilisation de ces énergies, les opérateurs clés, les prix du gaz, l'électricité, et le stockage de gaz. L'objectif est de fournir un aperçu global de l'évolution énergétique en France au cours de cette période.
""")

st.write(""" Les données proviennet du site datagouv.fr """)

# Lire le fichier CSV en spécifiant le délimiteur comme la tabulation
@st.cache_data

def load_data():
    df1 = pd.read_csv('conso-elec-gaz-annuelle-par-naf-agregee-region.csv', delimiter=';')  
    return df1
df1 = load_data()

def load_data():
    df2 = pd.read_csv('evolution-des-prix-domestiques-du-gaz-et-de-lelectricite.csv', delimiter=';')  
    return df2
df2 = load_data()

def load_data():
    df3 = pd.read_csv('stock-quotidien-stockages-gaz.csv', delimiter=';')  
    return df3
df3 = load_data()



# ajout titre et dans le menu
st.markdown('<a id="Evolution-de-la-consommation-2011-à-2021"></a>', unsafe_allow_html=True)
st.header('Evolution de la consommation 2011 à 2021')

# Visualisations 

data_gaz = df1[df1['filiere'] == 'Gaz']
data_gaz = data_gaz.sort_values(by='annee')
data_electricite = df1[df1['filiere'] == 'Electricité']
data_electricite = data_gaz.sort_values(by='annee')

# Créez un graphique à barres Plotly pour l'évolution de la consommation de gaz

fig1 = px.bar(data_gaz, x='annee', y='conso', labels={'conso': 'Consommation de Gaz (MWh)'})

# Spécifiez la couleur verte
color = 'green'

fig1.update_traces(marker_color=color)


fig1.update_layout(
    title='Consommation de Gaz',
    xaxis_title='Année',
    yaxis_title='Gaz (MWh)',
    xaxis={'type': 'category'}
)

# Affichez le graphique dans Streamlit
st.plotly_chart(fig1)

# Créez un graphique à barres Plotly pour l'évolution de la consommation d'électricité
fig2 = px.bar(data_electricite, x='annee', y='conso', labels={'conso': 'Consommation Électricité (MWh)'})

fig2.update_layout(
    title='Consommation d\'Électricité',
    xaxis_title='Année',
    yaxis_title='Électricité (MWh)',
    xaxis={'type': 'category'}
)

# Affichez le graphique dans Streamlit
st.plotly_chart(fig2)

# ajout titre et dans le menu
st.markdown('<a id="Les-5-plus-grands-secteurs-de-la-consommation"></a>', unsafe_allow_html=True)
st.header('Les 5 plus grands secteurs de la consommation')

# Grouper les données par année et secteur pour le gaz
top_5_gaz = data_gaz.groupby(['annee', 'libelle_grand_secteur'])['conso'].sum().unstack().sum().nlargest(5)

# Grouper les données par année et secteur pour l'électricité
top_5_electricite = data_electricite.groupby(['annee', 'libelle_grand_secteur'])['conso'].sum().unstack().sum().nlargest(5)

# Fusionne les deux séries de données (gaz et électricité)
top_5_combined = top_5_gaz.add(top_5_electricite, fill_value=0)

# Crée un graphique à barres Plotly pour les 5 plus grands secteurs de consommation de gaz et d'électricité ensemble
fig3 = px.bar(top_5_combined, x=top_5_combined.index, y=top_5_combined.values, labels={'y':'Consommation (MWh)'})

# Spécifiez la couleur verte
color = 'purple'

fig3.update_traces(marker_color=color)

fig3.update_layout(
    title='Consommation de Gaz et d\'Électricité (2011-2021)',
    xaxis_title='Secteur',
    yaxis_title='Consommation (MWh)'
)
# Affiche le graphique dans Streamlit
st.plotly_chart(fig3)


# ajout titre et dans le menu
st.markdown('<a id="Les-5-principaux-opérateurs-de-consommation"></a>', unsafe_allow_html=True)
st.header('Les 5 principaux opérateurs de consommation ')




# Groupez les données par opérateur et calculez la consommation totale
aggregated_data = df1.groupby('operateur')['conso'].sum()

# Triez les opérateurs par consommation totale et sélectionnez les 5 principaux
top_operateurs = aggregated_data.sort_values(ascending=False).head(5)

# Créez un camembert interactif avec Plotly Express
fig4 = px.pie(
    names=top_operateurs.index,
    values=top_operateurs.values,
    width=800,
    
)

# Personnaliser la légende avec du CSS
st.markdown(
    """
    <style>
    .legend {
        font-size: 25px;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Personnalisez le texte affiché lors du survol de chaque section
fig4.update_traces(textinfo='percent+label')

# Affichez le camembert interactif dans Streamlit
st.plotly_chart(fig4)


# ajout titre et dans le menu
st.markdown('<a id="Comparaison-évolution-en-France-et-en-UE"></a>', unsafe_allow_html=True)
st.header('Comparaison évolution en France et en UE ')



data2_2011_2021 = df2.loc[(df2['annee'] >= 2011) & (df2['annee'] <= 2021) & (df2['semestre'] == 'S1')]
data2_2011_2021 = data2_2011_2021.sort_values(by='annee')

annees = data2_2011_2021['annee']
prix_france_s1 = data2_2011_2021['france_gaz_naturel']
prix_ue_s1 = data2_2011_2021['u_e_gaz_naturel']

# Créez un graphique interactif avec Plotly Express
fig5 = px.line(data2_2011_2021, x='annee', y=['france_gaz_naturel', 'u_e_gaz_naturel'], labels={'france_gaz_naturel': 'Prix en France', 'u_e_gaz_naturel': 'Prix dans l\'UE'})

# Personnalisez le graphique
fig5.update_traces(mode="lines+markers")
fig5.update_layout(
    title='Évolution du Prix du Gaz ',
    xaxis_title='Année',
    yaxis_title='Prix du Gaz en €/MWh'
)

st.plotly_chart(fig5)

prix_elecfr_s1 = data2_2011_2021['france_electricite']
prix_elecue_s1 = data2_2011_2021['u_e_electricite']

# Créez un graphique interactif avec Plotly Express
# Créez un graphique interactif avec Plotly Express
fig6 = px.line(data2_2011_2021, x='annee', y=['france_electricite', 'u_e_electricite'], labels={'france_electricite': 'France', 'u_e_electricite': 'UE'})


# Personnalisez le graphique
fig6.update_traces(mode="lines+markers")
fig6.update_layout(
    title='Évolution du Prix de l\'Electrcité ',
    xaxis_title='Année',
    yaxis_title='Prix de l\'électrcité en €/MWh'
)

st.plotly_chart(fig6)

# ajout titre et dans le menu
st.markdown('<a id="Évolution-de-stockage-de-Gaz-en-France"></a>', unsafe_allow_html=True)
st.header('Évolutionde stockage de Gaz en France')



# Convertir la colonne 'date' en format de date
df3['date'] = pd.to_datetime(df3['date'])

# Filtrer les données pour la période de 2011 à 2021
data3_2011_2021 = df3[(df3['date'] >= '2011-01-01') & (df3['date'] <= '2021-12-31')]

data3_2011_2021 = data3_2011_2021.sort_values(by='date')
# Regrouper les données par année et calculer la moyenne du stockage
stockage_moyen_par_annee = data3_2011_2021.groupby(data3_2011_2021['date'].dt.year)['stock_fin_de_journee'].mean()

fig7 = px.line(stockage_moyen_par_annee, x=stockage_moyen_par_annee.index, y=stockage_moyen_par_annee.values)

# Personnalisez le graphique
fig7.update_traces(mode="lines+markers", line=dict(color='black'))
fig7.update_layout(
    xaxis_title='Année',
    yaxis_title='GWh'
)

st.plotly_chart(fig7)