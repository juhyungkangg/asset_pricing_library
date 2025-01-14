# src/instruments/vanilla_option.py
from .instrument_base import Instrument


class VanillaOption(Instrument):
    def __init__(self,
                 strike: float,
                 maturity: float,
                 option_type: str,  # "call" or "put"
                 exercise_style: str = "european"):  # or "american"
        self.strike = strike
        self.maturity = maturity
        self.option_type = option_type
        self.exercise_style = exercise_style

    def get_pricing_parameters(self):
        return {
            "strike": self.strike,
            "maturity": self.maturity,
            "option_type": self.option_type,
            "exercise_style": self.exercise_style,
        }

    def accept_pricer(self, pricer):
        return pricer.price_vanilla_option(self)
