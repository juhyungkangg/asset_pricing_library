# src/market_data/market.py
class Market:
    """
    Encapsulates all market information needed to price instruments:
    - Spot prices
    - Discount curves
    - Vol surfaces
    - FX rates
    etc.
    """
    def __init__(self,
                 yield_curve: object,
                 vol_surface_dict: object = None,
                 spot_prices: object = None,
                 params: object = None) -> object:
        self.yield_curve = yield_curve
        self.vol_surface_dict = vol_surface_dict or {}
        self.spot_prices = spot_prices or {}
        self.params = params

    def get_spot_price(self, symbol: str):
        return self.spot_prices.get(symbol, None)

    def get_yield_curve(self):
        return self.yield_curve

    def get_vol_surface(self, symbol: str):
        return self.vol_surface_dict.get(symbol, None)
