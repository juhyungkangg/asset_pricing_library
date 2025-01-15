# Example pseudo-code usage:

from src.instruments.vanilla_option import VanillaOption
from src.instruments.barrier_option import BarrierOption
from src.models.black_scholes.black_scholes_pricing import BlackScholesEngine
from src.market_data.market import Market
from src.models.pde.pde_pricing import PDEPricingEngine
from src.valuation.valuation_request import ValuationRequest
from src.models.monte_carlo.monte_carlo_pricing import MonteCarloEngine

# 1. Create a Market object
market = Market(
    yield_curve=None,  # a yield curve object or mock
    vol_surface_dict={},
    fx_spot_rates={"STOCK_XYZ": 100.0}
)

# 2. Construct an Instrument
eu_call_option = VanillaOption(
    strike=100,
    maturity=1.0,        # 1 year
    option_type="call",
    exercise_style="european"
)

# 2. Construct an Instrument
eu_put_option = VanillaOption(
    strike=100,
    maturity=1.0,        # 1 year
    option_type="put",
    exercise_style="european"
)

# 3. Choose a Pricing Engine
bs_engine = BlackScholesEngine(
    interest_rate=0.02,
    volatility=0.20,
    spot_price=market.get_spot_price("STOCK_XYZ"),
    dividend_yield=0.0
)

mc_engine = MonteCarloEngine(
    interest_rate=0.02,
    volatility=0.20,
    spot_price=market.get_spot_price("STOCK_XYZ"),
    dividend_yield=0.0,
    n_paths=1000000,
    n_steps=252
)

pde_engine = PDEPricingEngine(
    interest_rate=0.02,
    volatility=0.20,
    spot_price=market.get_spot_price("STOCK_XYZ"),
    dividend_yield=0.0,
    nx=2200,
    nt=252
)

# 4. Create a Valuation Request
valuation_req = ValuationRequest(
    instrument=eu_call_option,
    pricer=bs_engine,
    market=market
)

# # 5. Run valuation
# fair_value = valuation_req.run_valuation()
# print("Fair Value:", fair_value)
#
# valuation_req = ValuationRequest(
#     instrument=eu_call_option,
#     pricer=mc_engine,
#     market=market
# )
# fair_value = valuation_req.run_valuation()
# print("Fair Value:", fair_value)

# # 4. Create a Valuation Request
# valuation_req = ValuationRequest(
#     instrument=eu_put_option,
#     pricer=bs_engine,
#     market=market
# )
#
# # 5. Run valuation
# fair_value = valuation_req.run_valuation()
# print("Fair Value:", fair_value)
#
# valuation_req = ValuationRequest(
#     instrument=eu_put_option,
#     pricer=mc_engine,
#     market=market
# )
# fair_value = valuation_req.run_valuation()
# print("Fair Value:", fair_value)


# valuation_req = ValuationRequest(
#     instrument=eu_call_option,
#     pricer=pde_engine,
#     market=market
# )
# fair_value = valuation_req.run_valuation()
# print("Fair Value:", fair_value)


barrier_call_option = BarrierOption(
    strike=110,
    maturity=1.0,
    option_type="call",
    barrier_level=80,
    barrier_type="down-and-out"
)

valuation_req = ValuationRequest(
    instrument=barrier_call_option,
    pricer=bs_engine,
    market=market
)
fair_value = valuation_req.run_valuation()
print("Fair Value:", fair_value)

# valuation_req = ValuationRequest(
#     instrument=barrier_call_option,
#     pricer=mc_engine,
#     market=market
# )
# fair_value = valuation_req.run_valuation()
# print("Fair Value:", fair_value)

valuation_req = ValuationRequest(
    instrument=barrier_call_option,
    pricer=pde_engine,
    market=market
)
fair_value = valuation_req.run_valuation()
print("Fair Value:", fair_value)
