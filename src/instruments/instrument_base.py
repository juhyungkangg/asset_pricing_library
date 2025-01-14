# src/instruments/instrument_base.py
from abc import ABC, abstractmethod

class Instrument(ABC):
    """
    Abstract base class for all financial instruments.
    """
    @abstractmethod
    def get_pricing_parameters(self):
        """
        Returns the necessary parameters to price this instrument:
        - Underlying(s)
        - Tenor / Maturity
        - Payoff details
        - Optional specifics (barrier, etc.)
        """
        pass

    @abstractmethod
    def accept_pricer(self, pricer):
        """
        Double-dispatch pattern to allow the pricer (model) to
        handle this specific instrument type.
        """
        pass
