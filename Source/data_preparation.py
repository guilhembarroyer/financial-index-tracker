"""Data Preparation Module"""

import pandas as pd

import threading
import time


try:
    import logging

    import yfinance as yf

    logging.disable(logging.ERROR)

    ENABLE_YFINANCE = True
except ImportError:
    ENABLE_YFINANCE = False

try:
    from tqdm import tqdm

    ENABLE_TQDM = True
except ImportError:
    ENABLE_TQDM = False



def get_historical_data(
    tickers: list[str] | str,
    ticker_type: str = "stock",
    start: str | None = "01/01/2010",
    end: str | None = "28/10/2022",
    source_path: str = "/Users/guilhembarroyer/Desktop/Projects/financial-index-tracker/InputFiles/data.xlsx",
    rounding: int | None = None,
    sleep_timer: bool = True,
    show_ticker_seperation: bool = True,
    show_errors: bool = True,
    tqdm_message: str = "Obtaining historical data",
    progress_bar: bool = True,
):
   
    def worker(ticker, historical_data_dict):
        historical_data = pd.DataFrame()
       
        if ticker in excel_tickers:
            historical_data = get_historical_data_from_excel(
                ticker=ticker,
                ticker_type=ticker_type,
                source_path=source_path,
            )

            if not historical_data.empty:
                excel_tickers.append(ticker)

        if historical_data.empty or ticker not in excel_tickers:
            if ENABLE_YFINANCE:
                historical_data = get_historical_data_from_yahoo_finance(
                    ticker=ticker,
                    start=start,
                    end=end,
                    interval=interval,
                    return_column=return_column,
                    risk_free_rate=risk_free_rate,
                    divide_ohlc_by=divide_ohlc_by,
                )

            if not historical_data.empty:
                yf_tickers.append(ticker)

        if historical_data.empty:
            no_data.append(ticker)
        if not historical_data.empty:
            historical_data_dict[ticker] = historical_data

    if isinstance(tickers, str):
        ticker_list = [tickers]
    elif isinstance(tickers, list):
        ticker_list = tickers
    else:
        raise ValueError(f"Type for the tickers ({type(tickers)}) variable is invalid.")

    ticker_list_iterator = (
        tqdm(ticker_list, desc=tqdm_message)
        if (ENABLE_TQDM & progress_bar)
        else ticker_list
    )

    historical_data_dict: dict[str, pd.DataFrame] = {}
    excel_tickers: list[str] = []
    yf_tickers: list[str] = []
    no_data: list[str] = []
    threads = []

    for ticker in ticker_list_iterator:
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



    if excel_tickers and yf_tickers and show_ticker_seperation:
        print(
            f"The following tickers acquired historical data from the xlsx data file: {', '.join(excel_tickers)}"
        )
        print(
            f"The following tickers acquired historical data from YahooFinance: {', '.join(yf_tickers)}"
        )

    if no_data and show_errors:
        if not ENABLE_YFINANCE:
            print(
                "Due to a missing optional dependency (yfinance) and the current data file, "
                f"data for the following tickers could not be acquired: {', '.join(no_data)}\n"
                "Enable this functionality by using:\033[1m pip install 'financetoolkit[yfinance]' \033[0m"
            )
        else:
            print(f"No data found for the following tickers: {', '.join(no_data)}")

    if len(historical_data_dict) == 0:
        print("No data found in your conditions.")

    reorder_tickers = [ticker for ticker in tickers if ticker in historical_data_dict]

    if not historical_data_dict:
        raise ValueError("No data found for the given tickers.")

    historical_data = pd.concat(historical_data_dict).unstack(level=0)
    historical_data = historical_data.reindex(reorder_tickers, level=1, axis=1)



    if rounding:
        historical_data = historical_data.round(rounding)

    return historical_data, no_data




def get_historical_data_from_excel(ticker, ticker_type, source_path ):
    if(source_path):
        if ticker_type == "stock":
            historical_data=pd.DataFrame(
            data=0,
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
            ],
        )
            stocks_description_df = pd.read_excel(source_path, sheet_name="Members")
            if ticker in stocks_description_df.iloc[:, 0].values:    
                values = stocks_description_df.loc[stocks_description_df.iloc[:, 0] == ticker, 1:5].values.flatten()
                historical_data.loc[1, ["Name", "Bics1", "Bics2", "Bics3", "Bics4"]] = values
                
                print(historical_data.head())    
    return 


get_historical_data_from_excel("AAPL UW","stock", "/Users/guilhembarroyer/Desktop/Projects/financial-index-tracker/InputFiles/data.xlsx")

