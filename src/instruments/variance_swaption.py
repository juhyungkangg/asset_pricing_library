# src/instruments/variance_swaption.py
from .instrument_base import Instrument

class Variance_Swaption(Instrument):
    def __init__(self,
                 notional: float,
                 strike_rate: float,
                 maturity: float,
                 option_type: str,  # "payer" or "receiver"
                 underlying_swap_tenor: float):
        """
        - 'option_type' can be 'payer' (like a call on interest rates) or 'receiver' (like a put).
        - 'underlying_swap_tenor' is how long the swap runs once exercised.
        """
        self.notional = notional
        self.strike_rate = strike_rate
        self.maturity = maturity
        self.option_type = option_type
        self.underlying_swap_tenor = underlying_swap_tenor

    def get_pricing_parameters(self):
        return {
            "notional": self.notional,
            "strike_rate": self.strike_rate,
            "maturity": self.maturity,
            "option_type": self.option_type,
            "underlying_swap_tenor": self.underlying_swap_tenor
        }

    def accept_pricer(self, pricer):
        return pricer.price_variance_swaption(self)
