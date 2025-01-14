import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from engine_controller import Controller

# Initialisation du Controller
controller = Controller()
source_path=controller.excel_path


# Initialisation de la session state
if "page" not in st.session_state:
    st.session_state.page = "data"

# Page de sélection de l'univers
if st.session_state.page == "data":
    
    

    # Titre de l'application
    st.title("Chargement de données")

    # Entrée pour que l'utilisateur écrive le chemin de son fichier
    source_path = st.text_input("Entrez le chemin de votre fichier de données :",source_path)

    if source_path is not None:
        try:
            infos_df=pd.read_excel(source_path, sheet_name="Qualitativ_2018")
            members_df = pd.read_excel(source_path, sheet_name="Members")
            controller.excel_path = source_path
            st.success("Fichier chargé avec succès !")
        except Exception as e:
        
            st.error(f"Erreur lors de la lecture du fichier : {e}") 


    st.title("Univers de l'Indice - Filtres Géographique et Sectoriel")



    infos_df.rename(columns={infos_df.columns[0]: "TICKER"}, inplace=True)


    index_list=["S&P 500", "Stoxx"]
    selected_index = st.multiselect("Sélectionnez un indice :", index_list, index_list)

    countries_by_index = {
        "S&P 500": ["US"],
        "Stoxx": list(infos_df[infos_df["COUNTRY"]!="US"]["COUNTRY"].dropna().unique())
        #["AS", "BD", "BE", "CL", "DE", "F+", "FI", "FR", "GB", "GE", "IR","IS", "IT", "JO", "LX", "MB", "NE", "NO", "PD","SP", "SW", "SZ"]
    }
    countries=countries_by_index["S&P 500"]+countries_by_index["Stoxx"]
    countries_filtered = []
    for index in selected_index:
        countries_filtered+=countries_by_index[index]
    selected_countries = st.multiselect("Sélectionnez les pays :", countries, countries_filtered)



    members_df.columns = ['SPX Index', 'NAME', 'BICS_LEVEL_1_SECTOR_NAME', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME', 'BICS_LEVEL_3_INDUSTRY_NAME', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME', '', 'SXXP Index', 'NAME_bis', 'BICS_LEVEL_1_SECTOR_NAME_bis', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis', 'BICS_LEVEL_3_INDUSTRY_NAME_bis', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis']
    if selected_index==["S&P 500"]:
        members_df['SPX Index', 'NAME', 'BICS_LEVEL_1_SECTOR_NAME', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME', 'BICS_LEVEL_3_INDUSTRY_NAME', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME']= None
    elif selected_index==["S&P 500"]:
        members_df['SXXP Index', 'NAME_bis', 'BICS_LEVEL_1_SECTOR_NAME_bis', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis', 'BICS_LEVEL_3_INDUSTRY_NAME_bis', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis']= None


    bics1 = np.union1d(
        members_df['BICS_LEVEL_1_SECTOR_NAME'].dropna().unique(),
        members_df['BICS_LEVEL_1_SECTOR_NAME_bis'].dropna().unique()
    )
    selected_bics1 = st.multiselect("Sélectionnez les niveaux BICS 1 :", bics1, bics1, key="bics1")


    bics2 = np.union1d(
        members_df['BICS_LEVEL_2_INDUSTRY_GROUP_NAME'].dropna().unique(),
        members_df['BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis'].dropna().unique()
    )
    bics2_filtered=[]
    for bic1 in selected_bics1:
        bics2_filtered+=list(np.union1d(
            members_df[members_df['BICS_LEVEL_1_SECTOR_NAME']==bic1]['BICS_LEVEL_2_INDUSTRY_GROUP_NAME'].dropna().unique(),
            members_df[members_df['BICS_LEVEL_1_SECTOR_NAME_bis']==bic1]['BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis'].dropna().unique()))
    selected_bics2 = st.multiselect("Sélectionnez les niveaux BICS 2 :", bics2, bics2_filtered, key="bics2")


    bics3 = np.union1d(
        members_df['BICS_LEVEL_3_INDUSTRY_NAME'].dropna().unique(),
        members_df['BICS_LEVEL_3_INDUSTRY_NAME_bis'].dropna().unique()
    )
    bics3_filtered=[]
    for bic2 in selected_bics2:
        bics3_filtered+=list(np.union1d(
            members_df[members_df['BICS_LEVEL_2_INDUSTRY_GROUP_NAME']==bic2]['BICS_LEVEL_3_INDUSTRY_NAME'].dropna().unique(),
            members_df[members_df['BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis']==bic2]['BICS_LEVEL_3_INDUSTRY_NAME_bis'].dropna().unique()))
    selected_bics3 = st.multiselect("Sélectionnez les niveaux BICS 3 :", bics3, bics3_filtered, key="bics3")


    bics4 = np.union1d(
        members_df['BICS_LEVEL_4_SUB_INDUSTRY_NAME'].dropna().unique(),
        members_df['BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis'].dropna().unique()
    )
    bics4_filtered=[]
    for bic3 in selected_bics3:
        bics4_filtered+=list(np.union1d(
            members_df[members_df['BICS_LEVEL_3_INDUSTRY_NAME']==bic3]['BICS_LEVEL_4_SUB_INDUSTRY_NAME'].dropna().unique(),
            members_df[members_df['BICS_LEVEL_3_INDUSTRY_NAME_bis']==bic3]['BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis'].dropna().unique()))
    selected_bics4 = st.multiselect("Sélectionnez les niveaux BICS 4 :", bics4, bics4_filtered, key="bics4")

    st.title("Sélection de l'Univers Final parmis la sélection de Tickers Filtrés")

    univers_tickers_list=infos_df.iloc[:,0].dropna().unique()
    univers_tickers_filtered=[]
    members_df = pd.read_excel(source_path, sheet_name="Members")
    members_df.columns = ['SPX Index', 'NAME', 'BICS_LEVEL_1_SECTOR_NAME', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME', 'BICS_LEVEL_3_INDUSTRY_NAME', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME', '', 'SXXP Index', 'NAME_bis', 'BICS_LEVEL_1_SECTOR_NAME_bis', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis', 'BICS_LEVEL_3_INDUSTRY_NAME_bis', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis']
    for ticker in  univers_tickers_list:
        if infos_df[infos_df["TICKER"]==ticker]["COUNTRY"].values[0] in selected_countries:
            if members_df[members_df["SPX Index"]==ticker]["BICS_LEVEL_4_SUB_INDUSTRY_NAME"].values in selected_bics4 or members_df[members_df["SXXP Index"]==ticker]["BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis"].values in selected_bics4:
                univers_tickers_filtered.append(ticker)
    selected_tickers = st.multiselect("Sélectionnez les tickers constituant l'Univers final de votre Indice", univers_tickers_list, univers_tickers_filtered, key="tickers")



    # Mettre à jour l'attribut `.tickers` du controller
    if st.button("Mettre à jour l'univers et passer à la création de l'indice"):
        try:
            controller.update_universe(selected_tickers)
            st.success(f"Univers mis à jour! Vous pouvez créer des indices allant jusqu'à {len(selected_tickers)} valeurs.")
            
            st.session_state.page = "indice"
            st.success("Cliquez de nouveau pour continuer.")

        except ValueError as e:
            st.error(f"Erreur : {e}")

# Page de création de l'indice
elif st.session_state.page == "indice":
    st.title("Création de l'Indice")
    st.write("Bienvenue sur la page de création de l'indice !")
    
    index_type = st.selectbox(
            "Choisissez le type d'indice :",
            options=["Indice basé sur des critères qualitatifs", "Indice basé sur les cours historiques"],
        )
    st.write("Les indidices basés sur les cours historiques sont plus longs à calculer, ils sont ainsi limités à 30 valeurs contre 100 pour les autres.")

    if index_type == "Indice basé sur des critères qualitatifs":
        max_value = 100
        options_rebalancing = ["Aucun", "Rééquilibrage annuel", "Rééquilibrage continu"]
        rebalancing_after_2020=False
    elif index_type == "Indice basé sur les cours historiques":
        max_value = 30
        options_rebalancing = ["Aucun", "Rééquilibrage annuel"]
        rebalancing_after_2020=True
        
    index_size = st.number_input(
        "Nombre de valeurs dans l'indice :",
        min_value=5,
        max_value=max_value,
        value=20,
        step=1
    )
    

    rebalancing=st.selectbox("Choisissez la fréquence de rééquilibrage :", options=options_rebalancing)


    if rebalancing_after_2020:
        last_datetime=datetime(2021, 12, 31)
    else:
        last_datetime=datetime(2020, 12, 31)

    creation_date=st.date_input(
    "Date de création de l'indice.",
    value=datetime(2018, 1, 1),  # Valeur par défaut
    min_value=datetime(2018, 1, 1),  # Date minimale
    max_value=last_datetime  # Date maximale
    )

    end_tracking_date=st.date_input(
    "Date de création de l'indice.",
    value=datetime(2020, 12, 31),  # Valeur par défaut
    min_value=creation_date,  # Date minimale
    max_value=datetime(2022, 12, 31)  # Date maximale
    )

    if not rebalancing_after_2020:
        st.write("Il n'y a pas de rebalancement possible après 2020, vous pouvez tracker des indices jusqu'en 2022 mais il s'agira d'un indice modifié en 2020 au maximum.")
   
    st.write("Analyse de l'adaptabilité des indices à vos critères")


    analyse_upload=False

    if st.button("Analyse"):
        try:
            results=controller.choose_index(index_type, index_size, rebalancing, creation_date, end_tracking_date)
            st.success("Analyse terminée !")
            analyse_upload=True
            
        
        except ValueError as e:
            st.error(f"Erreur : {e}")
    
    if analyse_upload:
        st.write("Les configurations d'indices disponibles sont les suivantes :")   
