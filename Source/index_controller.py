import numpy as np
import pandas as pd
from datetime import datetime, date

class Index:
    def __init__(
            self,
            tickers: list[str] | None = None,
            historical_data: dict[str, pd.DataFrame] | None = None,
            selection_type: str="Équipondéré",
            index_choice: str = "Market Cap Index",
            index_size: int=15, 
            dividend: str | list[str] | bool | None = True,
    ):
        self.tickers = tickers 
        self.selection_type = selection_type
        self.index_size = index_size
        self.index_choice = index_choice
        self.historical_data=historical_data
        self.dividend = dividend
 


    def update_available_config(self,
                                index_choice: str="qualitative",
    ):  
        tickers=self.tickers
        universe_data= self.historical_data
        if universe_data is None or universe_data.empty:
            raise ValueError("Le paramètre 'universe_data' ne doit pas être vide ou nul. Il y a un problème de récupération des données.")
        
        if index_choice == "qualitative":
            years=[2018, 2019,  2020]
            configurations= {'dividends': {},'Market Cap Index': {}, 'Growth Index(PB)':{}, 'Value Index(PB)':{}, 'Value Index(PE)': {},'Growth Index(PE)':{}, 'Dividend Yield Index':{}}
            
            print(self.dividend)
            for year in years:
                for ticker in tickers:
                    
                    if self.dividend==False and universe_data[f"DVD_FREQ_{year}"][ticker][0]!=None:
                        
                        if year not in configurations['dividends']:
                            configurations['dividends'][year]=[]
                        configurations['dividends'][year].append(ticker)
                        

                    
                    
                    elif self.dividend!=False:
                        add=True
                        for dividend_type in self.dividend:
                            if dividend_type=="Irréguliers" and universe_data[f"DVD_FREQ_{year}"][ticker][0]=="Irreg":
                                add=False
                            elif dividend_type=="Annuels" and universe_data[f"DVD_FREQ_{year}"][ticker][0]=="Annual":
                                add=False
                            elif dividend_type=="Semestriels" and universe_data[f"DVD_FREQ_{year}"][ticker][0]=="Semi-Anl":
                                add=False
                            elif dividend_type=="Trimestriels" and universe_data[f"DVD_FREQ_{year}"][ticker][0]=="Quarter":
                                add=False
                        if add:
                            if year not in configurations['dividends']:
                                configurations['dividends'][year]=[]
                            configurations['dividends'][year].append(ticker)
                       
            
            
            
            
            
            for ticker in tickers:
                
                for year in years:
                    if pd.isna(universe_data[f"PX_TO_BOOK_RATIO_{year}"][ticker][0]):
                        configurations['Growth Index(PB)'][year]=[]
                        configurations['Growth Index(PB)'][year].append(ticker) 
                        configurations['Value Index(PB)'][year]=[]
                        configurations['Value Index(PB)'][year].append(ticker) 
                    if pd.isna(universe_data[f"PE_RATIO_{year}"][ticker][0]):
                        configurations['Growth Index(PE)'][year]=[]
                        configurations['Value Index(PE)'][year]=[]
                        configurations['Growth Index(PE)'][year].append(ticker)
                        configurations['Value Index(PE)'][year].append(ticker) 
                    if pd.isna(universe_data[f"CUR_MKT_CAP_{year}"][ticker][0]):
                        configurations['Market Cap Index'][year]=[]
                        configurations['Market Cap Index'][year].append(ticker)
                    if pd.isna(universe_data[f"EQY_DVD_YLD_IND_{year}"][ticker][0]):
                        configurations['Dividend Yield Index'][year]=[]
                        configurations['Dividend Yield Index'][year].append(ticker)


        
        elif index_choice=="historical_prices":
            configurations={'global': None,'Low Volatility Index': None, 'Momentum Index': None}
        
        print(configurations)
        return configurations



    def allocate_values_in_index(self,
        rebalancing: str="Aucun",
        ):  
        self.rebalancing = rebalancing
        
        historical_data_df=self.historical_data
        index_choice=self.index_choice
        ponderation=self.selection_type
        index_size=self.index_size

        print(ponderation)

        if index_choice=="Market Cap Index":
            prefix="CUR_MKT_CAP_"
            max_min=True
        elif index_choice=="Growth Index(PB)":
            prefix="PX_TO_BOOK_RATIO_"
            max_min=True
        elif index_choice=="Growth Index(PE)":
            prefix="PE_RATIO_"
            max_min=True
        elif index_choice=="Value Index(PB)":
            prefix="PX_TO_BOOK_RATIO_"
            max_min=False
        elif index_choice=="Value Index(PE)":
            prefix="PE_RATIO_"
            max_min=False
        elif index_choice=="Dividend Yield Index":
            prefix="EQY_DVD_YLD_IND_"
            max_min=True

        if rebalancing=="Aucun":
            if max_min:
                results_df=historical_data_df.nlargest(index_size, prefix+'2018')

                if ponderation=="Équipondéré":
                    results_df["Weight"]=1/len(results_df)

                elif ponderation=="Pondéré":
                    results_df["Weight"]=results_df[prefix+'2018']/results_df[prefix+'2018'].sum()
                    
            else:
                results_df=historical_data_df.nsmallest(index_size, prefix+'2018')
                
                if ponderation=="Équipondéré":
                    results_df["Weight"]=1/len(results_df)

                elif ponderation=="Pondéré":
                    results_df["Inverse_Weight"]=1/results_df[prefix+'2018']
                    results_df["Weight"]=results_df["Inverse_Weight"]/results_df["Inverse_Weight"].sum()

          
            return {"all_period_long":results_df}
        
        elif rebalancing=="Rééquilibrage annuel":

            results={}
            for year in [2018, 2019, 2020]:
                if max_min:
                    results_df=historical_data_df.nlargest(index_size, prefix+str(year))

                    if ponderation=="Équipondéré":
                        results_df["Weight"]=1/len(results_df)

                    elif ponderation=="Pondéré":
                        results_df["Weight"]=results_df[prefix+str(year)]/results_df[prefix+str(year)].sum()
                        
                else:
                    results_df=historical_data_df.nsmallest(index_size, prefix+str(year))
                    
                    if ponderation=="Équipondéré":
                        results_df["Weight"]=1/len(results_df)

                    elif ponderation=="Pondéré":
                        results_df["Inverse_Weight"]=1/results_df[prefix+str(year)]
                        results_df["Weight"]=results_df["Inverse_Weight"]/results_df["Inverse_Weight"].sum()

                results[str(year)]=results_df

            
            return results
      
