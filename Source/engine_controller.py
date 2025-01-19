"""Controller Module"""

import pandas as pd
from datetime import datetime, date
import numpy as np

from data_preparation import get_historical_data as _get_historical_data
from index_controller import Index

class Controller:

    def __init__(
        self,
        excel_path: str | None = "/Users/guilhembarroyer/Desktop/Projects/financial-index-tracker/InputFiles/data.xlsx",
        tickers: list[str] | None = None,
        historical_data: dict[str, pd.DataFrame] | None = None,
    ):
        self.excel_path = excel_path
        self.tickers = tickers if tickers is not None else []
        self.historical_data = historical_data if historical_data is not None else {}
        

        
    def update_universe(self, new_tickers):
        """Met à jour la liste des tickers après validation."""
        if not isinstance(new_tickers, list):
            raise ValueError("Les tickers doivent être fournis sous forme de liste.")
        self.tickers = new_tickers # Exemple : mettre en majuscules
        print(f"Tickers actuels : {self.tickers}")
        
    
    
    def get_historical_data(
        self,
        tickers: list[str] | None = None,
        research_type: str = "stock_info",
    ):
        
        if tickers is None:
            tickers = self.tickers  # Utilise les tickers du contrôleur si non spécifié.

        source_path = self.excel_path  # Utilise `excel_path` par défaut.
    
        universe_data, excel_tickers, no_data, *_  =_get_historical_data(tickers, source_path=source_path, research_type=research_type)
        
        if research_type=="stock_info":
            self.historical_data=universe_data

        return universe_data, excel_tickers, no_data
    

    def choose_index(
            self,
            index_type: str = "qualitative",
            #index_size: int | None = None,
            #rebalancing: str="Aucun",
            dividend: str | list[str] | bool = False,  
            ):
        
        
        tickers = self.tickers  

        universe_data, excel_tickers, no_data=self.get_historical_data(tickers, research_type="stock_info")
        
        index=Index(historical_data=universe_data, tickers=excel_tickers, dividend=dividend) #index_size=index_size,rebalancing=rebalancing,
        
        index_creation_constraints=index.update_available_config(index_choice=index_type) #, tickers=excel_tickers)
        
   

        return index_creation_constraints, excel_tickers, no_data



    def create_index(
            self,
            rebalancing: str | None = "Aucun",
            index_size: int = 15,
            tickers_index_list: list[str] | None = None,
            index_choice: str = "Market Cap Index",
            selection_type: str ="Équipondéré",
            selected_currency: str="USD",
            visual_continuous: bool=True,
            selected_benchmarks: list[str] | None = None,
    ):
        if selected_currency=="USD" or selected_currency=="EUR":
            currencies=["EURUSD"]
        elif selected_currency=="GBP":
            currencies=["EURGBP","USDGBP"]
        elif selected_currency=="JPY":
            currencies=["EURJPY","USDJPY"]
        elif selected_currency=="CNY":
            currencies=["EURCNY","USDCNY"]
        elif selected_currency=="CAD":
            currencies=["EURCAD","USDCAD"]
        
        
        

        currencies_df, excel_tickers, no_data=self.get_historical_data(tickers=currencies, research_type="currencies")

        data_df=self.convert_filter_data(selected_tickers=tickers_index_list,index_choice=index_choice, currencies_data_df=currencies_df, currency=selected_currency)

        final_index=Index(historical_data=data_df, tickers=tickers_index_list, index_size=index_size, index_choice=index_choice, selection_type=selection_type)
        
        index_composition_init=final_index.allocate_values_in_index(rebalancing=rebalancing)
        
        

        if visual_continuous:

       
            

            if rebalancing=="Aucun":

                index_composition=index_composition_init["all_period_long"]
               
                tickers_index_list=index_composition["Ticker"].tolist()
                
                prices_data, tickers, no_data=self.get_historical_data(tickers_index_list, research_type="stock_prices")
                
                prices = pd.DataFrame()
                weights = {}

                
                for ticker in tickers_index_list:
                    prices[ticker]=prices_data["Prices"][ticker]
                    weights[ticker]=index_composition[index_composition["Ticker"]==ticker]["Weight"].iloc[0] 
                    

                
         
                indice_values = prices.apply(lambda x: sum(x[ticker] * weights[ticker] for ticker in prices.columns), axis=1)
                

                first_ticker=tickers_index_list[0]
                
                index_df=pd.DataFrame({
                                        "Date": prices_data["Dates"][first_ticker],
                                        f"Indice ({selected_currency})": indice_values,
                                    })
                
                if len(selected_benchmarks)>0 and "None" not in selected_benchmarks:

                    benchmarks_data, tickers, no_data=self.get_historical_data(selected_benchmarks, research_type="benchmarks", )
                    
                    for benchmark in selected_benchmarks:
                        index_df[benchmark]=benchmarks_data[benchmark][benchmark]
                        index_df[benchmark]=(index_df[benchmark]/index_df[benchmark].iloc[0])*100

                index_df["Indice normalisé"]=(index_df[f"Indice ({selected_currency})"]/index_df[f"Indice ({selected_currency})"].iloc[0])*100

                
                index_df.set_index("Date", inplace=True)
                
                print(index_df)

                return index_df, index_composition_init, rebalancing
                    





            elif rebalancing=="Rééquilibrage annuel":
               
                final_index_df = pd.DataFrame()

                start_date=pd.to_datetime("28-12-2018")
                mid1_date=pd.to_datetime("30-12-2019")
                mid2_date=pd.to_datetime("30-12-2020")
                end_date=pd.to_datetime("30-12-2021")
                
                for year in [2018, 2019, 2020]:
                
                    index_composition=index_composition_init[f"{year}"]

                    tickers_index_list=index_composition["Ticker"].tolist()
                    
                    prices_data, tickers, no_data=self.get_historical_data(tickers_index_list, research_type="stock_prices")
                    
                    prices = pd.DataFrame()
                    weights = {}

                    
                    for ticker in tickers_index_list:
                        prices[ticker]=prices_data["Prices"][ticker]
                        weights[ticker]=index_composition[index_composition["Ticker"]==ticker]["Weight"].iloc[0] 
                        

                    
                    indice_values = prices.apply(lambda x: sum(x[ticker] * weights[ticker] for ticker in prices.columns), axis=1)
                    

                    first_ticker=tickers_index_list[0]
                    

                    index_df=pd.DataFrame({
                                            "Date": prices_data["Dates"][first_ticker],
                                            "Values": indice_values,
                                        })
                    
                    index_df['Date'] = pd.to_datetime(index_df['Date'])
                    print(index_df)
                    
                    if year == 2018:
                        filtered_df = index_df[(index_df['Date'] >= start_date) & (index_df['Date'] <= mid1_date)]
                    elif year == 2019:
                        filtered_df = index_df[(index_df['Date'] >= mid1_date) & (index_df['Date'] <= mid2_date)]
                    elif year == 2020:
                        filtered_df = index_df[(index_df['Date'] >= mid2_date) & (index_df['Date'] <= end_date)]
                    
                    filtered_df = filtered_df.rename(columns={"Values": f"Indice ({selected_currency})"})
                    final_index_df = pd.concat([final_index_df, filtered_df], ignore_index=True)

                    print('aaa', final_index_df)

                final_index_df.set_index("Date", inplace=True)

                if len(selected_benchmarks)>0 and "None" not in selected_benchmarks:

                    benchmarks_data, tickers, no_data=self.get_historical_data(selected_benchmarks, research_type="benchmarks", )
                    
                    for benchmark in selected_benchmarks:
                        index_df[benchmark]=benchmarks_data[benchmark][benchmark]
                        index_df[benchmark]=(index_df[benchmark]/index_df[benchmark].iloc[0])*100

                final_index_df["Indice normalisé"]=(final_index_df[f"Indice ({selected_currency})"]/final_index_df[f"Indice ({selected_currency})"].iloc[0])*100

                print(final_index_df)
                return final_index_df, index_composition_init, rebalancing             
       
        


        pass

    
    def convert_filter_data(
            self,
            selected_tickers: list[str],
            index_choice: str, 
            currencies_data_df: pd.DataFrame, 
            currency: str
        ) -> pd.DataFrame:

        raw_data_df=self.historical_data
        
        
        results_df=pd.DataFrame(columns=[
                        "Ticker",
                        "Name",
                        "Country",
                        "PX_LAST_2018",
                        "PX_LAST_2019",
                        "PX_LAST_2020",
                    ])
        


        for ticker in selected_tickers:

            new_row = pd.DataFrame({
                'Ticker':[ticker],
                'Name': ["Name"],
                'Bics1': ["Bics1"],
                'Country': ['Country_name'],  
                'PX_LAST_2018': [None],
                'PX_LAST_2019': [None],
                'PX_LAST_2020': [None],
            })

            new_row["Name"][0]=raw_data_df["Name"][ticker][0]
            new_row["Bics1"][0]=raw_data_df["Bics1"][ticker][0]
            new_row["Country"][0]=raw_data_df["Country"][ticker][0]

            currency_convert=False
            invert=False
            if raw_data_df["Country"][ticker][0]=="US":
                if currency=="EUR":
                    currency_convert=True
                    currency_ticker="EURUSD"
                    invert=True

                elif currency!=("USD" or "EUR"):
                    currency_convert=True
                    currency_ticker="USD"+currency
            else:
                if currency=="USD":
                    currency_convert=True
                    currency_ticker="EURUSD"
                elif currency!=("USD" or "EUR"):
                    currency_convert=True
                    currency_ticker="USD"+currency
            
            currency_data_df=currencies_data_df[[("Dates",currency_ticker ), ("Values", currency_ticker)]]
            currency_data_df.columns=["Dates", "Values"]

            if currency_convert:
                convert_values={"30-12-2018":currency_data_df[currency_data_df["Dates"]=="28-12-2018"]["Values"], "30-12-2019":currency_data_df[currency_data_df["Dates"]=="28-12-2018"]["Values"], "30-12-2020": currency_data_df[currency_data_df["Dates"]=="30-12-2020"]["Values"]}
                if invert:
                    convert_values["30-12-2018"]=1/convert_values["30-12-2018"]
                    convert_values["30-12-2019"]=1/convert_values["30-12-2019"]
                    convert_values["30-12-2020"]=1/convert_values["30-12-2020"]
            else:
                convert_values={"30-12-2018":1, "30-12-2019":1, "30-12-2020": 1}


            for year in [2018, 2019, 2020]:
                
                new_row[f"PX_LAST_{year}"][0]=raw_data_df[f"PX_LAST_{year}"][ticker][0]*convert_values[f"30-12-{year}"]

                if index_choice=="Market Cap Index":
                    new_row[f"CUR_MKT_CAP_{year}"]=0
                    new_row[f"CUR_MKT_CAP_{year}"][0]=raw_data_df[f"CUR_MKT_CAP_{year}"][ticker][0]*convert_values[f"30-12-{year}"]
                elif index_choice=="Growth Index(PB)" or index_choice=="Value Index(PB)":
                    new_row[f"PX_TO_BOOK_RATIO_{year}"]=0
                    new_row[f"PX_TO_BOOK_RATIO_{year}"][0]=raw_data_df[f"PX_TO_BOOK_RATIO_{year}"][ticker][0]
                elif index_choice=="Growth Index(PE)" or index_choice=="Value Index(PE)":
                    new_row[f"PE_RATIO_{year}"]=0
                    new_row[f"PE_RATIO_{year}"][0]=raw_data_df[f"PE_RATIO_{year}"][ticker][0]
                if index_choice=="Dividend Yield Index":
                    new_row[f"EQY_DVD_YLD_IND_{year}"]=0
                    new_row[f"EQY_DVD_YLD_IND_{year}"][0]=raw_data_df[f"EQY_DVD_YLD_IND_{year}"][ticker][0]*convert_values[f"30-12-{year}"]

            results_df = pd.concat([results_df, new_row], ignore_index=True)

        

        return results_df