# src/models/pricing_engine_base.py
from abc import ABC, abstractmethod

class PricingEngine(ABC):
    """
    Abstract class that defines the methods to price different instruments.
    """

    @abstractmethod
    def price_vanilla_option(self, vanilla_option):
        pass

    @abstractmethod
    def price_barrier_option(self, barrier_option):
        pass

    @abstractmethod
    def price_fx_barrier_option(self, fx_barrier_option):
        pass

    @abstractmethod
    def price_variance_swap_swaption(self, swaption):
        pass
