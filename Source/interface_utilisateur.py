import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import linregress
import plotly.express as px

from engine_controller import Controller

def create_pie_chart(data, column, title):
        fig = px.pie(data, values="Weight", names=column, title=title)
        return fig

# Initialisation du Controller
controller = Controller()
source_path=controller.excel_path


# Initialisation de la session state
if "page" not in st.session_state:
    st.session_state.page = "data"


if "controller" not in st.session_state:
    st.session_state.controller = Controller() 
controller = st.session_state.controller

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


    if len(selected_tickers)<5:
        raise ValueError("Il n'y a pas assez de valeurs pour constituer un indice, il en faut au moins 5.")
    # Mettre à jour l'attribut `.tickers` du controller
    if st.button("Mettre à jour l'univers et passer à la création de l'indice"):
        try:

            controller.update_universe(selected_tickers)
            st.success(f"Univers mis à jour! Vous pouvez créer des indices allant jusqu'à {len(controller.tickers)} valeurs.")

            st.session_state.page = "indice"
            st.success(f"Cliquez de nouveau pour continuer.")

        except ValueError as e:
            st.error(f"Erreur : {e}")



# Page de création de l'indice
elif st.session_state.page == "indice":
    if "tickers" not in st.session_state:
        st.session_state.tickers = controller.tickers
    if "losses" not in st.session_state:
        st.session_state.losses = {}
    if "no_data" not in st.session_state:
        st.session_state.no_data = []

    if "analyse_upload" not in st.session_state:
        st.session_state.analyse_upload = False

    st.title("Paramétrage de l'Indice")
    st.write("Bienvenue sur la page de création de l'indice !")
    
    index_type = st.selectbox(
            "Choisissez le type d'indice :",
            options=["Indice basé sur des critères qualitatifs", "Indice basé sur les cours historiques"],
        )
    st.write("Les indidices basés sur les cours historiques sont plus longs à calculer, ils sont ainsi limités à 30 valeurs contre 100 pour les autres.")

    if index_type == "Indice basé sur des critères qualitatifs":
        index_type="qualitative"
        if len(controller.tickers)>=100:
            max_value = 100
        else:
            max_value=len(controller.tickers)
        options_rebalancing = ["Aucun", "Rééquilibrage annuel"]
       

    elif index_type == "Indice basé sur les cours historiques":
        index_type="historical_prices"
        if len(controller.tickers)>=30:
            max_value = 30
        else:
            max_value=len(controller.tickers)
        options_rebalancing = ["Aucun", "Rééquilibrage annuel", "Rééquilibrage continu"]
        rebalancing_after_2020=True

    index_size = st.number_input(
        "Nombre de valeurs dans l'indice :",
        min_value=5,
        max_value=max_value,
        value=max_value,
        step=1
    )
    

    rebalancing=st.selectbox("Choisissez la fréquence de rééquilibrage :", options=options_rebalancing)


    

    has_dividends = st.checkbox("Inclure les actions versant des divdendes?", value=True)

    # Gestion des choix en fonction de l'état de `has_dividends`
    if has_dividends:
        st.write("Veuillez sélectionner les types de dividendes à inclure.")
        
        # Liste des options de types de dividendes
        dividend_types = [
            "Irréguliers",
            "Annuels",
            "Semestriels",
            "Trimestriels"
        ]
        selected_dividends = st.multiselect(
            "Types de dividendes",
            options=dividend_types,
            default=dividend_types
        )
        
        # Afficher la sélection
        if selected_dividends:
            st.success(f"Types de dividendes sélectionnés : {', '.join(selected_dividends)}")
        else:
            st.warning("Veuillez sélectionner au moins un type de dividende.")
    else:
        st.write("Aucun dividende ne sera inclus.")
        selected_dividends=False


        
    st.write("Analyse de l'adaptabilité des indices à vos critères")

    
    
  
    ticker_losses={'dividends': {},'Market Cap Index': {}, 'Growth Index(PB)': {} , 'Growth Index(PE)': {} , 'Value Index(PB)': {}, 'Value Index(PE)': {},'Dividend Yield Index':{}}
    excel_tickers=[]
    no_data=[]

    options_index=['Market Cap Index','Growth Index(PB)', 'Growth Index(PE)', 'Value Index(PB)', 'Value Index(PE)', 'Dividend Yield Index']   

    index_choice=st.selectbox("Choix du type d'indice", options_index)
    
    st.write("Pensez à bien lancer l'analyse avant de poursuivre vers la création de l'indice!")
    if st.button("Analyse"):
        try:
            st.session_state.analyse_upload = False
            ticker_losses, excel_tickers, no_data, *_=controller.choose_index(index_type=index_type,  dividend=selected_dividends)
            st.session_state.tickers=excel_tickers
            st.session_state.losses=ticker_losses
            st.session_state.no_data=no_data
            st.success(f"Analyse terminée !")
            st.write(f"{ticker_losses}")
            st.session_state.analyse_upload = True
            
            
        
        except ValueError as e:
            st.error(f"Erreur : {e}")



    if st.session_state.analyse_upload:
   
        excel_tickers=st.session_state.tickers
        ticker_losses=st.session_state.losses
        no_data=st.session_state.no_data
        if len(no_data)>0:
            st.write(f"Pas de données pour ces {len(no_data)} valeurs: {no_data}.")
            if len(excel_tickers)-len(no_data)<index_size:
                st.write("Pas assez de données pour constituer l'indice, diminuez la taille souhaitée de l'indice  ou élargissez l'univers de l'indice.")
                st.write("Actualisez la page pour revenir sur la page de création de l'univers des valeurs")
        
        
        year_with_issue=[]
        for year in [2018, 2019, 2020]:
            if year in ticker_losses['dividends']:
                if len(excel_tickers)-(len(ticker_losses['dividends'][year])+len(no_data))<index_size:
                    year_with_issue.append(year)
        
        if len(year_with_issue)>0:
            st.write(f"Pas assez de valeurs correspondantes pour constituer l'indice dans les conditions sur les dividendes demandées en {year_with_issue}: diminuez la taille souhaitée de l'indice souhaité, changez la politique de dividendes, révisez la période de tracking ou élargissez l'univers de l'indice.")
            st.write("Actualisez la page pour revenir sur la page de création de l'univers des valeurs")

        else: 
            
            not_available_tickers=no_data
            for year in [2018, 2019, 2020]:
                available_tickers=len(excel_tickers)
                if year in ticker_losses["dividends"]:
                    not_available_tickers=not_available_tickers+ticker_losses["dividends"][year]
                if year in ticker_losses[index_choice]:
                    not_available_tickers=not_available_tickers+ticker_losses[index_choice][year]
            not_available_tickers = list(set(not_available_tickers))
            

            if available_tickers-len(not_available_tickers)<index_size:
                st.write(f"Pas assez de données/valeurs correspondantes pour créer un indice \"{index_choice}\" dans les conditions demandées sur l'année {year}: changez le typen d'indice voulu les paramètres de taille, de dividendes, révisez la période de tracking ou élargissez l'univers de l'indice.")
                st.write("Actualisez la page pour revenir sur la page de création de l'univers des valeurs")

            else:

            

                tickers_index_list=[]
                index_choice_list=[]
                dividend_choice_list=[]
                for ticker in excel_tickers:
                    added=False
                    for year in [2018, 2019, 2020]:
                        if year in ticker_losses[index_choice]:   
                            if ticker in ticker_losses[index_choice][year] and (ticker not in index_choice_list and ticker not in dividend_choice_list):
                                index_choice_list.append(ticker)
                                added=True
                        if year in ticker_losses['dividends']:   
                            if ticker in ticker_losses['dividends'][year] and ( ticker not in index_choice and ticker not in dividend_choice_list):
                                dividend_choice_list.append(ticker)
                                added=True
                    if not added:
                        tickers_index_list.append(ticker)
                st.session_state.final_tickers=tickers_index_list
                
            

                st.write(f"L'univers de création de votre indice est de (réduit à) {len(tickers_index_list)} correspondant aux valeurs suivantes: {tickers_index_list}.")
                st.write(f"""Les autres valeurs ont été abandonnées du fait:
                -{len(no_data)} du fait d'absence de données: {no_data};
                -{len(dividend_choice_list)} du fait de la politique de dividende choisie: {dividend_choice_list};
                -{len(index_choice_list)} du fait du type d'indice choisi: {index_choice_list}""")
                

                selection_type=st.selectbox("Mode de répartition des valeurs:", ["Équipondéré", "Pondéré"])    


                

            
                st.write("Voulez-vous un ou plusieurs benchmarks pour comparer la performance?")
                
                # Liste des options de types de dividendes
                benchmarks_options = [
                    "SPX",
                    "SXXP",
                    "None"
                ]
                selected_benchmarks = st.multiselect(
                    "Types de dividendes",
                    options=benchmarks_options,
                    default="None"
                )
                if "None" in selected_benchmarks and len(selected_benchmarks) > 1:
                    st.warning("Vous ne pouvez pas sélectionner 'None' avec d'autres benchmarks.")
                    # Supprime les autres benchmarks pour ne garder que "None"
                    selected_benchmarks = ["None"]

                # Afficher la sélection
                if selected_benchmarks:
                    st.success(f"Benchmarks sélectionnés : {', '.join(selected_benchmarks)}")
                else:
                    st.warning("Veuillez sélectionner au moins une option.")
            

                st.write("Dans quelle devise souhaitez-vous les valeurs de sorties de l'indice?")
                selected_currency=st.selectbox("Choix de la devise de sortie:", ["USD", "EUR",  "CAD", "CNY", "GBP", "JPY"])
                
                
                
                
                if st.button("Création de l'indice"):
                    try:
                       #controller.tickers=st.session_state.final_tickers
                        
                        st.session_state.results=controller.create_index(tickers_index_list=st.session_state.final_tickers, rebalancing=rebalancing, index_size=index_size, index_choice=index_choice,  selected_benchmarks=selected_benchmarks, selected_currency=selected_currency, selection_type=selection_type)

                        st.success(f"Analysez la performance de l'indice paramétré")
                        
                        st.session_state.page = "visual"
                        st.success(f"Cliquez de nouveau pour continuer.")
                                
                                
                    
                    except ValueError as e:
                        st.error(f"Erreur : {e}")


elif st.session_state.page == "visual": 
    resultats_indice, composition_indice, rebalancing=st.session_state.results
    
    resultats_indice['Rendements de l\'indice'] = resultats_indice['Indice normalisé'].pct_change()

    # Interface utilisateur Streamlit
    st.title("Composition de l'indice par année")

    # Itération sur les années
    for year, df in composition_indice.items():
        st.subheader(f"Année {year}")
        
    # Graphiques
        st.plotly_chart(create_pie_chart(df, "Name", f"Proportions par valeur ({year})"))
        st.plotly_chart(create_pie_chart(df, "Country", f"Proportions par pays ({year})"))
        st.plotly_chart(create_pie_chart(df, "Bics1", f"Proportions par secteur ({year})"))



    performance_totale = (resultats_indice['Indice normalisé'].iloc[-1] / resultats_indice['Indice normalisé'].iloc[0]) - 1
    performance_annualisee = (1 + performance_totale) ** (365 / len(resultats_indice)) - 1
    volatilite = resultats_indice['Rendements de l\'indice'].std() * np.sqrt(252)
    max_drawdown = ((resultats_indice['Indice normalisé'] / resultats_indice['Indice normalisé'].cummax()) - 1).min()
    taux_sans_risque = st.number_input('Choisissez le taux sans risque pour le calcul du ratio de Sharpe:', min_value=0.0, max_value=0.1, value=0.02, step=0.001)
    sharpe_ratio = (performance_annualisee - taux_sans_risque) / volatilite
 

    # Résumé des indicateurs
    indicateurs = pd.DataFrame({
        'Indicateur': ['Performance Totale', 'Performance Annualisée', 'Volatilité', 'Max Drawdown', 'Sharpe Ratio'],
        'Valeur': [performance_totale, performance_annualisee, volatilite, max_drawdown, sharpe_ratio]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=resultats_indice.index, y=resultats_indice['Indice normalisé'], mode='lines', name='Index', line=dict(color='blue')))

    if "SPX" in resultats_indice.columns:
        resultats_indice['Rendement du SPX'] = resultats_indice['SPX'].pct_change()
        betaSPX, alphaSPX, _, _, _ = linregress(resultats_indice['Rendement du SPX'].dropna(), resultats_indice['Rendements de l\'indice'].dropna())
        fig.add_trace(go.Scatter(x=resultats_indice.index, y=resultats_indice['SPX'], mode='lines', name='SPX', line=dict(color='orange')))
        indicateurs = pd.concat([indicateurs,pd.DataFrame({'Indicateur': ['Beta SPX'], 'Valeur': betaSPX})], ignore_index=True)
        indicateurs = pd.concat([indicateurs, pd.DataFrame({'Indicateur': ['Alpha SPX'], 'Valeur': alphaSPX})], ignore_index=True)


    if "SXXP" in resultats_indice.columns:
        resultats_indice['Rendement du SXXP'] = resultats_indice['SXXP'].pct_change()
        betaSXXP, alphaSXXP, _, _, _ = linregress(resultats_indice['Rendement du SXXP'].dropna(), resultats_indice['Rendements de l\'indice'].dropna())
        fig.add_trace(go.Scatter(x=resultats_indice.index, y=resultats_indice['SXXP'], mode='lines', name='SXXP', line=dict(color='orange')))

        indicateurs = pd.concat([indicateurs,pd.DataFrame({'Indicateur': ['Beta SXXP'], 'Valeur': betaSXXP})], ignore_index=True)
        indicateurs = pd.concat([indicateurs,pd.DataFrame({'Indicateur': ['Alpha SXXP'], 'Valeur': alphaSXXP})], ignore_index=True)

    st.title("Résultats de la performance de votre indice")
    st.dataframe(resultats_indice)

    fig.update_layout(title="Évolution des indices", xaxis_title="Date", yaxis_title="Valeur de l'indice")
    st.markdown("### Visualisation de l'Indice")
    st.markdown("""
    Le graphique ci-dessous montre l'évolution de l'indice au fil du temps. 
    Vous pouvez l'utiliser pour suivre la performance globale de votre indice.
    """)
    st.plotly_chart(fig, use_container_width=True)

    st.table(indicateurs)

  
    pass

