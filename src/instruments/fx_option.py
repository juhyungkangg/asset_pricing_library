# src/instruments/fx_option.py
from .barrier_option import BarrierOption

class FXBarrierOption(BarrierOption):
    def __init__(self,
                 strike: float,
                 maturity: float,
                 option_type: str,
                 barrier_level: float,
                 barrier_type: str,
                 domestic_ccy: str,    # e.g., "USD"
                 foreign_ccy: str,     # e.g., "EUR"
                 notional: float,
                 rebate: float = 0.0):
        super().__init__(strike, maturity, option_type, barrier_level, barrier_type, rebate)
        self.domestic_ccy = domestic_ccy
        self.foreign_ccy = foreign_ccy
        self.notional = notional

    def get_pricing_parameters(self):
        params = super().get_pricing_parameters()
        params.update({
            "domestic_ccy": self.domestic_ccy,
            "foreign_ccy": self.foreign_ccy,
            "notional": self.notional,
        })
        return params

    def accept_pricer(self, pricer):
        return pricer.price_fx_barrier_option(self)
