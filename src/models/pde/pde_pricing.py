# src/models/pde_pricing.py

import numpy as np
from src.models.pricing_engine_base import PricingEngine
from .pde_functions import *
from ..black_scholes.black_scholes_functions import barrier_option_price_bs

class PDEPricingEngine(PricingEngine):
    def __init__(self,
                 interest_rate: float,
                 volatility: float,
                 spot_price: float,
                 dividend_yield: float = 0.0,
                 nx: int = 200,
                 nt: int = 252,):
        """
        PDE Pricing Engine using a Black-Scholes setup
        :param interest_rate:
        :param volatility:
        :param spot_price:
        :param dividend_yield:
        :param nx:
        :param nt:
        """
        self.r = interest_rate
        self.sigma = volatility
        self.S0 = spot_price
        self.q = dividend_yield
        self.nx = nx
        self.nt = nt

    def price_vanilla_option(self, vanilla_option) -> float:
        T = vanilla_option.maturity
        K = vanilla_option.strike
        option_type = vanilla_option.option_type
        x_max = self.S0 * 3

        return vanilla_option_price_pde(self.S0, K, T, self.r, self.sigma, option_type, x_max, self.nx, self.nt)

    def price_barrier_option(self, barrier_option):
        T = barrier_option.maturity
        K = barrier_option.strike
        B = barrier_option.barrier_level
        barrier_type = barrier_option.barrier_type
        option_type = barrier_option.option_type

        return barrier_option_price_pde(self.S0, K, T, self.r, self.sigma, B, option_type, barrier_type, self.nx, self.nt)


    def price_fx_barrier_option(self, fx_barrier_option):
        """
        TODO: Implement a specialized FX barrier PDE if needed.
        """
        raise NotImplementedError("FX Barrier pricing not yet implemented.")

    def price_variance_swap_swaption(self, swaption):
        """
        TODO: Implement a variance swap(tion) PDE if needed.
        """
        raise NotImplementedError("Variance swaption pricing not yet implemented.")