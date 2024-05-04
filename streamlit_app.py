### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime   
from utils.create_table import create_table


### CONFIGURATION ###
st.set_page_config(
    page_title="Simulateur Prêt Immobilier 🏠",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


## HEADER ##
st.title("🏠 Simulateur Prêt Immobilier 🏠")
st.write('Ce simulateur vous permet de calculer les mensualités de votre prêt immobilier en fonction de différents paramètres.')


## SIDE BAR
st.sidebar.image('./img/image.jpg', use_column_width="auto")
st.sidebar.title("🔍 Filtres crédit 🔍")

defaut_montant = 250000
if 'filtre_montant' not in st.session_state:
    st.session_state.number_input_value = defaut_montant
filtre_montant = st.sidebar.number_input("Montant de l'emprunt (en €)", value=defaut_montant, min_value=10000, step=5000)
st.session_state.filtre_montant = filtre_montant

defaut_taux = 3.5
if 'filtre_taux' not in st.session_state:
    st.session_state.number_input_value = defaut_taux
filtre_taux = st.sidebar.number_input("Taux d'intérêt (en %)", value=defaut_taux, min_value=0.1, step=0.05) / 100
st.session_state.filtre_taux = filtre_taux

defaut_duree = 20
if 'filtre_duree' not in st.session_state:
    st.session_state.number_input_value = defaut_duree
filtre_duree = st.sidebar.number_input("Durée de l'emprunt (en années)", value=defaut_duree, min_value=1, step=1)
st.session_state.filtre_duree = filtre_duree

initial_date_debut_pret = pd.to_datetime(datetime.now().date()) + pd.offsets.MonthBegin(1)
if 'filtre_date_debut_pret' not in st.session_state:
    st.session_state.date_input_value = initial_date_debut_pret
filtre_date_debut_pret = st.sidebar.date_input("Date de début du prêt (1er paiement)", value=initial_date_debut_pret, format = 'DD-MM-YYYY')
st.session_state.filtre_date_debut_pret = filtre_date_debut_pret

defaut_assurance = 0.2
if 'filtre_assurance' not in st.session_state:
    st.session_state.number_input_value = defaut_assurance
filtre_assurance = st.sidebar.number_input("Taux de l'assurance (en %)", value=defaut_assurance, step=0.05) / 100
st.session_state.filtre_assurance = filtre_assurance


## CHARGEMENT DES DONNEES ##
data = create_table(taux = st.session_state.filtre_taux, 
                    emprunt = st.session_state.filtre_montant, 
                    duree = st.session_state.filtre_duree, 
                    taux_assurance = st.session_state.filtre_assurance, 
                    date_debut_pret = st.session_state.filtre_date_debut_pret)


## APPLICATION ##
st.subheader("📈 Statistiques du crédit 📈")
st.write('Ci-dessous, vous trouverez les statistiques du crédit en fonction des filtres paramétrés')

columns = st.columns(5)

with columns[0]:
    st.metric(label = "Montant de l'emprunt", value = f"{st.session_state.filtre_montant:,.0f} €".replace(',', ' '))
    st.metric(label = "Coût total crédit", value = f"{data['mensualite_globale'].sum():,.0f} €".replace(',', ' '))
    st.metric(label = "% coût total / emprunt", value = f"{data['mensualite_globale'].sum() / st.session_state.filtre_montant * 100:.2f} %")

    
with columns[1]:
    st.metric(label = "Mensualité globale", value = f"{data['mensualite_globale'].iloc[0]:,.0f} €".replace(',', ' '))
    st.metric(label = "Mensualité moyenne capital", value = f"{data['mensualite_capital'].mean():,.0f} €".replace(',', ' '))
    st.metric(label = "Mensualité moyenne intérêts", value = f"{data['mensualite_interet'].mean():,.0f} €".replace(',', ' '))
    
with columns[2]:
    st.metric(label = "Taux d'intérêt", value = f"{st.session_state.filtre_taux * 100:.2f} %")
    st.metric(label = "Coût total intérêts", value = f"{data['mensualite_interet'].sum():,.0f} €".replace(',', ' '))
    st.metric(label = "% intérêts / coût total", value = f"{data['mensualite_interet'].sum() / data['mensualite_globale'].sum() * 100:.2f} %")

    
with columns[3]:
    st.metric(label = "Durée de l'emprunt", value = f"{st.session_state.filtre_duree} ans")
    st.metric(label = "Date fin de remboursement", value = data['date_remboursement'].iloc[-1].strftime('%h %Y'))
    
with columns[4]:
    st.metric(label = "Taux d'assurance", value = f"{st.session_state.filtre_assurance * 100:.2f} %")
    st.metric(label = "Coût total assurance", value = f"{data['mensualite_assurance'].sum():,.0f} €".replace(',', ' '))
    st.metric(label = "Mensualité assurance", value = f"{data['mensualite_assurance'].iloc[0]:,.0f} €".replace(',', ' '))



st.write('---')

st.subheader("📊 Affichage du tableau d'amortissement 📊")
st.write('Vous pouvez afficher les données en cliquant sur le bouton ci-dessous. Vous pourrez ensuite les exporter au format CSV.')
affichage_data = st.toggle(label = "Afficher les données")
if affichage_data:
    st.dataframe(data, use_container_width = True)
    st.write('Nombre de mensualités :', data.shape[0])