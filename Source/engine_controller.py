"""Controller Module"""

import pandas as pd

from data_preparation import get_historical_data as _get_historical_data

from Indices.index_controller import Index

class Controller:

    def __init__(
        self,
        excel_path: str | None = "/Users/guilhembarroyer/Desktop/Projects/financial-index-tracker/InputFiles/data.xlsx",
        tickers: list[str] | None = None,
        historical_data: dict[str, pd.DataFrame] | None = None,
        tracking_start: int | None = None,
        length_tracking: int | None = None,
        benchmark_ticker: str | None = None,
        convert_currency: str | None = 'USD',
        rounding: int | None = 4,
    ):
        self.excel_path = excel_path
        self.tickers = tickers if tickers is not None else []
        self.historical_data = historical_data if historical_data is not None else {}
        self.tracking_start = tracking_start
        self.length_tracking = length_tracking
        self.benchmark_ticker = benchmark_ticker
        self.convert_currency = convert_currency
        self.rounding = rounding


        
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
    
        
        historical_data, no_data=_get_historical_data(tickers, source_path=source_path, research_type=research_type)
        
        if research_type=="stock_info":
            #présenter les configurations d'indice disponibles, les tickers sans
            print("yes")

        return historical_data, no_data
    

    def choose_index(
            self,
            index_type: str = "discrete_rebalanced",
            index_size=30
    ):
        
        index=Index(universe=self.tickers, index_type=index_type, index_size=index_size)
        
        index_creation_constraints=index.update_available_config()

        return index_creation_constraints


    def create_index(
            self,
            index_type: str = "discrete_rebalanced",
            index_size=30,
            convert_currency: str | None = None,
            benchmark_ticker: str | None = None,
            tracking_start: int | None = None,
            length_tracking: int | None = None,
            rounding: int | None = None
    ):
        pass