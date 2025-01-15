# src/instruments/variance_swaption.py
from .instrument_base import Instrument

class Variance_Swap_Swaption(Instrument):
    def __init__(self,
                 K: float,
                 T1: float,
                 T2: float,):
        """
        - 'option_type' can be 'payer' (like a call on interest rates) or 'receiver' (like a put).
        - 'underlying_swap_tenor' is how long the swap runs once exercised.
        """
        self.K = K
        self.T1 = T1
        self.T2 = T2

    def get_pricing_parameters(self):
        return {
            "Strike": self.K,
            "T1": self.T1,
            "T2": self.T2,
        }

    def accept_pricer(self, pricer):
        return pricer.price_variance_swap_swaption(self)
