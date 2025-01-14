# src/valuation/valuation_result.py
class ValuationResult:
    """
    Could store the computed fair value, greeks, scenario breakdown, etc.
    """
    def __init__(self, fair_value, greeks=None, additional_info=None):
        self.fair_value = fair_value
        self.greeks = greeks or {}
        self.additional_info = additional_info or {}
