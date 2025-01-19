"""Data Preparation Module"""

import pandas as pd

import threading
import time


#try:
 #   import logging

  #  import yfinance as yf

   # logging.disable(logging.ERROR)

   # ENABLE_YFINANCE = True
#except ImportError:
 #   ENABLE_YFINANCE = False



def get_historical_data(
    tickers: list[str] | str,
    research_type: str = "stock_info",
    source_path: str = "/Users/guilhembarroyer/Desktop/Projects/financial-index-tracker/InputFiles/data.xlsx",
    historical_prices: bool= False,
    #show_ticker_seperation: bool = True,
    show_errors: bool = True,
    tqdm_message: str = "Obtaining historical data",
    progress_bar: bool = True,
):
   
    def worker(ticker, historical_data_dict):
        
        historical_data = pd.DataFrame()
       
        
        historical_data = get_historical_data_from_excel(
            ticker=ticker,
            research_type=research_type,
            source_path=source_path,
            historical_prices=historical_prices,
        )

        if not historical_data.empty:
            excel_tickers.append(ticker)
        
        
        #if historical_data.empty or ticker not in excel_tickers:
         #   if ENABLE_YFINANCE:
          #      historical_data = get_historical_data_from_yahoo_finance(
           #         ticker=ticker,
            #        start=start,
             #       end=end,
              #      interval=interval,
               #     return_column=return_column,
                #    risk_free_rate=risk_free_rate,
                 #   divide_ohlc_by=divide_ohlc_by,
                #)

            #if not historical_data.empty:
             #   yf_tickers.append(ticker)
        

        elif historical_data.empty:
            no_data.append(ticker)
        if not historical_data.empty:
            historical_data_dict[ticker] = historical_data

    if isinstance(tickers, str):
        ticker_list = [tickers]
    elif isinstance(tickers, list):
        ticker_list = tickers
    else:
        raise ValueError(f"Type for the tickers ({type(tickers)}) variable is invalid.")

 

    historical_data_dict: dict[str, pd.DataFrame] = {}
    excel_tickers: list[str] = []
    #yf_tickers: list[str] = []
    no_data: list[str] = []
    threads = []
    

    for ticker in ticker_list:
        
        # Introduce a sleep timer to prevent rate limit errors
        time.sleep(0.1)

        thread = threading.Thread(
            target=worker,
            args=(ticker, historical_data_dict),
        )
        thread.start()
        threads.append(thread)
        
    for thread in threads:
        thread.join()



    #if excel_tickers and yf_tickers and show_ticker_seperation:
     #   print(
      #      f"The following tickers acquired historical data from the xlsx data file: {', '.join(excel_tickers)}"
       # )
       # print(
       #     f"The following tickers acquired historical data from YahooFinance: {', '.join(yf_tickers)}"
       # )

    if no_data and show_errors:
        #if not ENABLE_YFINANCE:
         #   print(
          #      "Due to a missing optional dependency (yfinance) and the current data file, "
           #     f"data for the following tickers could not be acquired: {', '.join(no_data)}\n"
            #    "Enable this functionality by using:\033[1m pip install 'financetoolkit[yfinance]' \033[0m"
            #)
        #else:
        print(f"No data found for the following tickers: {', '.join(no_data)}")

    
    if len(historical_data_dict) == 0:
        print("No data found in your conditions.")
    
    if not historical_data_dict:
        raise ValueError("No data found for the given tickers.")

    reorder_tickers = [ticker for ticker in tickers if ticker in historical_data_dict]
    
   
    historical_data_df = pd.concat(historical_data_dict).unstack(level=0)
    historical_data_df = historical_data_df.reindex(reorder_tickers, level=1, axis=1)

    return historical_data_df, excel_tickers, no_data


def get_historical_data_from_excel(ticker, research_type, source_path, historical_prices):

    if(source_path):
        in_excel=False
        if research_type == "stock_info" or research_type == "stock_prices":

            stocks_description_df = pd.read_excel(source_path, sheet_name="Members")
            stocks_description_df.columns = ['Index', 'NAME', 'BICS_LEVEL_1_SECTOR_NAME', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME', 'BICS_LEVEL_3_INDUSTRY_NAME', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME', '', 'SXXP Index', 'NAME_bis', 'BICS_LEVEL_1_SECTOR_NAME_bis', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis', 'BICS_LEVEL_3_INDUSTRY_NAME_bis', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis']

            if ticker in stocks_description_df.iloc[:, 0].values:   
                in_excel=True
                index="SPX"
                description_values = stocks_description_df.loc[stocks_description_df.iloc[:, 0] == ticker, ['NAME', 'BICS_LEVEL_1_SECTOR_NAME', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME', 'BICS_LEVEL_3_INDUSTRY_NAME', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME']].values.flatten()
                

            elif ticker in stocks_description_df.iloc[:, 7].values:    
                in_excel=True
                index="SXXP"
                description_values = stocks_description_df.loc[stocks_description_df.iloc[:, 7] == ticker, ['NAME_bis', 'BICS_LEVEL_1_SECTOR_NAME_bis', 'BICS_LEVEL_2_INDUSTRY_GROUP_NAME_bis', 'BICS_LEVEL_3_INDUSTRY_NAME_bis', 'BICS_LEVEL_4_SUB_INDUSTRY_NAME_bis']].values.flatten()
                
                
            else: 
                print(f"Ticker {ticker} not found in the data file")
                return {}

            if in_excel:
                if research_type == "stock_prices" or historical_prices:
                    px_data_df=pd.read_excel(source_path, sheet_name=f"{index}_PX_LAST")

                if research_type == "stock_prices":    

                    px_data_results_df=pd.DataFrame(columns=["Dates", "Prices"])
                    start_date=pd.to_datetime("28-12-2018")
                    end_date=pd.to_datetime("30-12-2021")
                    px_data_results_df["Dates"]=px_data_df[(px_data_df.iloc[:, 1] >= start_date) & (px_data_df.iloc[:, 1] <= end_date)].iloc[:, 1]
                    px_data_results_df["Prices"] = px_data_df[(px_data_df.iloc[:, 1] >= start_date) & (px_data_df.iloc[:, 1] <= end_date)][ticker]
                    px_data_results_df['Prices']=px_data_results_df['Prices'].fillna(method='ffill')
 

                    return px_data_results_df
                
                elif research_type == "stock_info" :
                    years = [2018, 2019, 2020]
                    qualitativ_data_result_df=pd.DataFrame(
                    columns=[
                        "Name",
                        "Bics1",
                        "Bics2",
                        "Bics3",
                        "Bics4",
                        "Country",
                        "PX_TO_BOOK_RATIO_2018",
                        "PX_TO_BOOK_RATIO_2019",
                        "PX_TO_BOOK_RATIO_2020",
                        "PE_RATIO_2018",
                        "PE_RATIO_2019",
                        "PE_RATIO_2020",
                        "CUR_MKT_CAP_2018",
                        "CUR_MKT_CAP_2019",
                        "CUR_MKT_CAP_2020",
                        "EQY_DVD_YLD_IND_2018",
                        "EQY_DVD_YLD_IND_2019",
                        "EQY_DVD_YLD_IND_2020",
                        "DVD_FREQ_2018",
                        "DVD_FREQ_2019",
                        "DVD_FREQ_2020",
                        "EQY_SH_OUT_2018",
                        "EQY_SH_OUT_2019",
                        "EQY_SH_OUT_2020",
                        "PX_LAST_2018",
                        "PX_LAST_2019",
                        "PX_LAST_2020",
                        "start_date",
                        "end_date"
                    ],)

                    qualitativ_data_result_df.loc[0, ["Name", "Bics1", "Bics2", "Bics3", "Bics4"]] = description_values
                    
                    if not historical_prices:
                        qualitativ_data_result_df["start_date"], qualitativ_data_result_df["end_date"]=None, None
                        
                    elif historical_prices:
                        qualitativ_data_result_df["start_date"]=px_data_df[ticker].first_valid_index()
                        qualitativ_data_result_df["end_date"]=px_data_df[ticker].last_valid_index()
                        

                    for year in years:
                        qualitativ_data_df = pd.read_excel(source_path, sheet_name=f"Qualitativ_{year}")

                        target_columns=["Country"]+list(f"{col}_{year}" for col in ['PX_TO_BOOK_RATIO', 'PE_RATIO', 'CUR_MKT_CAP', 'EQY_DVD_YLD_IND', "DVD_FREQ", "EQY_SH_OUT", 'PX_LAST'])
                        
                        if ticker in qualitativ_data_df.iloc[:, 0].values:
                            
                            values = qualitativ_data_df.loc[qualitativ_data_df.iloc[:, 0] == ticker, ['COUNTRY','PX_TO_BOOK_RATIO', 'PE_RATIO', 'CUR_MKT_CAP', 'EQY_DVD_YLD_IND', "DVD_FREQ", "EQY_SH_OUT", 'PX_LAST']].values.flatten()
                            
                            qualitativ_data_result_df.loc[0, target_columns] = values
                    
                    return qualitativ_data_result_df

        elif research_type=="currencies":
         
            forex_values_df=pd.DataFrame(
            columns=[
                "Dates",
                "Values"
            ],)

            currencies_df = pd.read_excel(source_path, sheet_name="Forex")
            start_date=pd.to_datetime("28-12-2018")
            end_date=pd.to_datetime("30-12-2021")
            forex_values_df["Dates"]=currencies_df[(currencies_df.iloc[:, 1] >= start_date) & (currencies_df.iloc[:, 1] <= end_date)].iloc[:, 1]
            forex_values_df["Values"] = currencies_df[(currencies_df.iloc[:, 1] >= start_date) & (currencies_df.iloc[:, 1] <= end_date)][ticker]


                
            return  forex_values_df

        
        

      

            
        elif research_type=="benchmarks":
            
            index_values_df=pd.DataFrame(
            columns=[
                "Dates"
            ],)
            index_description_df = pd.read_excel(source_path, sheet_name="Index")
            index_values_df["Dates"] = index_description_df["PX_LAST"]
            if ticker=="SPX" :   
                index_values_df["SPX"] = index_description_df["SPX Index"]
                in_excel=True
            elif ticker=="SXXP":    
                index_values_df["SXXP"] = index_description_df["SXXP Index"]
                in_excel=True
            else: 
                print(f"Ticker {ticker} not found in the data file")
            
            if in_excel:
                index_values_df=index_values_df.dropna()
                index_values_df=index_values_df.iloc[::-1].reset_index(drop=True)
                
            return  index_values_df

        return pd.DataFrame()
        


