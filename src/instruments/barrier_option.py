# src/instruments/barrier_option.py
from .vanilla_option import VanillaOption

class BarrierOption(VanillaOption):
    def __init__(self,
                 strike: float,
                 maturity: float,
                 option_type: str,
                 barrier_level: float,
                 barrier_type: str,     # "up-and-out", "down-and-in", etc.
                 rebate: float = 0.0):
        super().__init__(strike, maturity, option_type)
        self.barrier_level = barrier_level
        self.barrier_type = barrier_type
        self.rebate = rebate

    def get_pricing_parameters(self):
        params = super().get_pricing_parameters()
        params.update({
            "barrier_level": self.barrier_level,
            "barrier_type": self.barrier_type,
            "rebate": self.rebate
        })
        return params

    def accept_pricer(self, pricer):
        return pricer.price_barrier_option(self)
