# 0. Import modules
from src.instruments.vanilla_option import VanillaOption
from src.instruments.barrier_option import BarrierOption
from src.market_data.market import Market

from src.models.black_scholes.black_scholes_pricing import BlackScholesEngine
from src.models.pde.pde_pricing import PDEPricingEngine
from src.models.monte_carlo.monte_carlo_pricing import MonteCarloEngine

from src.valuation.valuation_request import ValuationRequest

# 1. Create a Market object
market = Market(
    yield_curve=None,  # a yield curve object or mock
    vol_surface_dict={},
    spot_prices={"STOCK_XYZ": 100.0}
)

# 2. Construct vanilla option Instruments

down_and_in_call_option = BarrierOption(
    strike=110,
    maturity=1.0,        # 1 year
    option_type="call",
    barrier_level=80,
    barrier_type="down_and_in",
)
down_and_out_call_option = BarrierOption(
    strike=110,
    maturity=1.0,        # 1 year
    option_type="call",
    barrier_level=80,
    barrier_type="down_and_out",
)

up_and_in_call_option = BarrierOption(
    strike=90,
    maturity=1.0,        # 1 year
    option_type="call",
    barrier_level=120,
    barrier_type="up_and_in",
)
up_and_out_call_option = BarrierOption(
    strike=90,
    maturity=1.0,        # 1 year
    option_type="call",
    barrier_level=120,
    barrier_type="up_and_out",
)

up_and_in_put_option = BarrierOption(
    strike=90,
    maturity=1.0,        # 1 year
    option_type="put",
    barrier_level=120,
    barrier_type="up_and_in",
)

up_and_out_put_option = BarrierOption(
    strike=90,
    maturity=1.0,        # 1 year
    option_type="put",
    barrier_level=120,
    barrier_type="up_and_out",
)

down_and_in_put_option = BarrierOption(
    strike=110,
    maturity=1.0,        # 1 year
    option_type="put",
    barrier_level=80,
    barrier_type="down_and_in",
)

down_and_out_put_option = BarrierOption(
    strike=110,
    maturity=1.0,        # 1 year
    option_type="put",
    barrier_level=80,
    barrier_type="down_and_out",
)

instruments = [down_and_in_call_option, down_and_out_call_option, up_and_in_call_option, up_and_out_call_option,
               down_and_in_put_option, down_and_out_put_option, up_and_in_put_option, up_and_out_put_option]
# instruments = [up_and_in_put_option, up_and_out_put_option]

# 3. Create Pricing Engines

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
    nx=500,
    nt=252
)

pricing_engines = [bs_engine, mc_engine, pde_engine]
# pricing_engines = [bs_engine, mc_engine]

# Print table header
print(
    f"{'Option Price':<15}{'Pricing Engine':<20}{'S0':<10}{'Sigma':<10}{'r':<10}{'Strike (K)':<15}{'Barrier (B)':<15}{'Maturity':<10}{'Option Type':<15}{'Barrier Type':<20}")
print("=" * 140)

# 4. Create a Valuation Request and run valuations
for instrument in instruments:
    # Get parameters
    strike = instrument.strike
    maturity = instrument.maturity
    option_type = instrument.option_type
    barrier_level = instrument.barrier_level
    barrier_type = instrument.barrier_type

    for pricing_engine in pricing_engines:
        # Get parameters
        pricing_engine_name = pricing_engine.__class__.__name__
        r = pricing_engine.r
        sigma = pricing_engine.sigma
        S0 = pricing_engine.S0

        valuation_req = ValuationRequest(instrument=instrument, pricer=pricing_engine, market=market)
        fair_value = valuation_req.run_valuation()

        # Print data in tabular format
        print(
            f"{round(fair_value, 4):<15}{pricing_engine_name:<20}{S0:<10}{sigma:<10}{r:<10}{strike:<15}{barrier_level:<15}{maturity:<10}{option_type:<15}{barrier_type:<15}")
