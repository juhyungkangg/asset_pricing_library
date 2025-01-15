# src/models/monte_carlo_pricing.py

import numpy as np
from src.models.pricing_engine_base import PricingEngine
from .monte_carlo_functions import *
from ..black_scholes.black_scholes_functions import barrier_option_price_bs


class MonteCarloEngine(PricingEngine):
    def __init__(self,
                 interest_rate: float,
                 volatility: float,
                 spot_price: float,
                 dividend_yield: float = 0.0,
                 n_paths: int = 10000,
                 n_steps: int = 252,
                 params: object = None):
        """
        Monte Carlo pricing engine using a Black-Scholes setup.

        Parameters
        ----------
        interest_rate : float
            The constant risk-free interest rate (r).
        volatility : float
            The constant volatility (sigma).
        spot_price : float
            Current spot price (S0).
        dividend_yield : float, optional
            Continuous dividend yield (q). Defaults to 0.0.
        """
        self.r = interest_rate
        self.sigma = volatility
        self.S0 = spot_price
        self.q = dividend_yield
        self.n_paths = n_paths
        self.n_steps = n_steps
        self.params = params

    def _simulate_paths_gbm(self, T):
        return simulate_paths_gbm(self.n_paths, self.n_steps, T, self.r, self.q, self.sigma, self.S0)

    def price_vanilla_option(self, vanilla_option) -> float:
        # Use the standard European BS formula
        if vanilla_option.exercise_style.lower() != "european":
            raise NotImplementedError("Black-ScholesEngine only supports European style in this example.")

        T = vanilla_option.maturity
        K = vanilla_option.strike
        option_type = vanilla_option.option_type

        # Simulate paths
        paths = self._simulate_paths_gbm(T)

        return vanilla_option_price_mc(paths, K, T, self.r, option_type)

    def price_barrier_option(self, barrier_option) -> float:
        T = barrier_option.maturity
        K = barrier_option.strike
        B = barrier_option.barrier_level
        rebate = barrier_option.rebate

        # Simulate paths
        paths = self._simulate_paths_gbm(T)

        return barrier_option_price_mc(paths, K, T, self.r, B, rebate, barrier_option.option_type,
                                       barrier_option.barrier_type)

    def price_fx_barrier_option(self, fx_barrier_option):
        """
        TODO: Implement a specialized FX barrier Monte Carlo if needed.
        """
        raise NotImplementedError("FX Barrier pricing not yet implemented.")

    def price_variance_swap_swaption(self, variance_swap_swaption):
        K = variance_swap_swaption.K
        T1 = variance_swap_swaption.T1
        T2 = variance_swap_swaption.T2

        return variance_swap_swaption_price_mc(self.S0, K, self.r, T1, T2, self.params, self.n_paths, self.n_steps)
