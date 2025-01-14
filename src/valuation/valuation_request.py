# src/valuation/valuation_request.py
from ..models.pricing_engine_base import PricingEngine
from ..instruments.instrument_base import Instrument
from ..market_data.market import Market

class ValuationRequest:
    def __init__(self,
                 instrument: Instrument,
                 pricer: PricingEngine,
                 market: Market):
        self.instrument = instrument
        self.pricer = pricer
        self.market = market

    def run_valuation(self):
        # Leverage the instrument's accept_pricer() method
        # or pass relevant market data to the pricer.
        return self.instrument.accept_pricer(self.pricer)
