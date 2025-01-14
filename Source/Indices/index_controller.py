import numpy as np
import pandas as pd

class Index:
    def __init__(
            self,
            universe=list[str],
            tickers: list[str] | None = None,
            historical_data: dict[str, pd.DataFrame] | None = None,
            tracking_start: int | None = None,
            length_tracking: int | None = None,
            benchmark_ticker: str | None = None,
            convert_currency: str | None = 'USD',
            rounding: int | None = 4,
    ):
        self.universe = universe
        self.tickers = tickers if tickers is not None else []
        self.historical_data = historical_data if historical_data is not None else {}
        self.tracking_start = tracking_start
        self.length_tracking = length_tracking
        self.benchmark_ticker = benchmark_ticker
        self.convert_currency = convert_currency
        self.rounding = rounding

    def update_available_config(self,
                                ):
        pass