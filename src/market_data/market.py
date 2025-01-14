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
                 yield_curve,
                 vol_surface_dict=None,
                 fx_spot_rates=None):
        self.yield_curve = yield_curve
        self.vol_surface_dict = vol_surface_dict or {}
        self.fx_spot_rates = fx_spot_rates or {}

    def get_spot_price(self, symbol: str):
        return self.fx_spot_rates.get(symbol, None)

    def get_yield_curve(self):
        return self.yield_curve

    def get_vol_surface(self, symbol: str):
        return self.vol_surface_dict.get(symbol, None)
