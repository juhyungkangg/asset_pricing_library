# Barrier & Exotic Options Pricing Library

This project provides a flexible framework for pricing a variety of financial derivatives, including:
- **Vanilla Options** (European-style calls and puts)
- **Barrier Options** (e.g., up-and-out, down-and-in)
- **FX Barrier Options** (extension of barrier options for foreign exchange)
- **Variance Swap Swaptions** (an exotic volatility derivative)

Multiple pricing approaches are demonstrated:
- **Analytical / Semi-Analytical** (via Black–Scholes formulas)
- **Finite Difference Methods** (PDE-based approach)
- **Monte Carlo Simulation** (GBM-based path simulation)

The repository is organized into modules for:
- **Instruments** (definition of payoff structures, barrier conditions, etc.)
- **Market Data** (spot prices, yields, vol surfaces, etc.)
- **Models** (various pricing engines implementing Black–Scholes, PDE, or Monte Carlo methods)
- **Utility Functions** (helper functions for calculations)
- **Valuation** (request/response classes to tie instruments, models, and market data together)
- **Examples** (Jupyter notebooks demonstrating how to use the library)

---

## Table of Contents
1. [Project Structure](#project-structure)  
2. [Getting Started](#getting-started)  
3. [Usage & Examples](#usage--examples)  
4. [Key Modules](#key-modules)  
5. [Contributing](#contributing)  
6. [License](#license)

---

## Project Structure

```
.
├── src
│   ├── instruments
│   │   ├── barrier_option.py
│   │   ├── fx_option.py
│   │   ├── instrument_base.py
│   │   ├── vanilla_option.py
│   │   └── variance_swaption.py
│   ├── market_data
│   │   └── market.py
│   ├── models
│   │   ├── black_scholes
│   │   │   ├── black_scholes_functions.py
│   │   │   └── black_scholes_pricing.py
│   │   ├── monte_carlo
│   │   │   ├── monte_carlo_functions.py
│   │   │   └── monte_carlo_pricing.py
│   │   ├── pde
│   │   │   ├── pde_functions.py
│   │   │   └── pde_pricing.py
│   │   └── pricing_engine_base.py
│   ├── utils
│   │   └── black_scholes_functions.py
│   └── valuation
│       ├── valuation_request.py
│       └── valuation_result.py
├── examples
│   ├── barrier_option_pricing.ipynb
│   ├── vanilla_option_pricing_ipynb
│   └── variance_swap_swaption_pricing.ipynb
└── README.md
```

- **`src/instruments`**: Contains instrument definitions (e.g. VanillaOption, BarrierOption, etc.).  
- **`src/market_data`**: Classes for encapsulating market data (spot, yield curves, vol surfaces, etc.).  
- **`src/models`**: Different pricing engines:
  - **Black–Scholes** (`black_scholes_pricing.py`)  
  - **Monte Carlo** (`monte_carlo_pricing.py`)  
  - **PDE** (`pde_pricing.py`)  
- **`src/utils`**: Utility functions for calculations and analytics.  
- **`src/valuation`**: Classes to orchestrate the pricing requests (ValuationRequest, ValuationResult).  
- **`examples`**: Jupyter notebooks demonstrating usage.

---

## Getting Started

### Prerequisites

- **Python 3.7+**
- Common Python libraries for numerical computing:
  - `numpy`
  - `scipy`
  - `tqdm`

### Installation

1. **Clone this repository**:
    ```bash
    git clone https://github.com/YourUserName/barrier-options-pricing.git
    cd barrier-options-pricing
    ```

2. **(Optional) Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/Mac
    # or 
    venv\Scripts\activate.bat  # On Windows
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have a `requirements.txt`, install the libraries manually, e.g. `pip install numpy scipy tqdm`.)*

---

## Usage & Examples

### Running the Example Notebooks

Inside the `examples/` directory, you will find three Jupyter notebooks:
- **`barrier_option_pricing.ipynb`**  
- **`vanilla_option_pricing_ipynb`**  
- **`variance_swap_swaption_pricing.ipynb`**

These notebooks demonstrate how to:
1. **Construct market data** (`Market` objects with spot prices, yield curves, etc.)  
2. **Define instruments** (e.g. `BarrierOption`, `VanillaOption`, `Variance_Swap_Swaption`)  
3. **Create pricing engines** (e.g. `BlackScholesEngine`, `MonteCarloEngine`, `PDEPricingEngine`)  
4. **Initiate a ValuationRequest** and retrieve the fair value of the instrument.

To run a notebook:
1. Ensure you’ve installed Jupyter (e.g., `pip install jupyter`)  
2. Navigate to the `examples/` folder:
    ```bash
    cd examples
    jupyter notebook
    ```
3. Open a `.ipynb` file (e.g., `barrier_option_pricing.ipynb`) and run all cells.

### Quick Code Snippet

Below is a simplified snippet for pricing a down-and-in call option using the Black–ScholesEngine:

```python
from src.instruments.barrier_option import BarrierOption
from src.market_data.market import Market
from src.models.black_scholes.black_scholes_pricing import BlackScholesEngine
from src.valuation.valuation_request import ValuationRequest

# 1. Market
market = Market(
    yield_curve=None,  # or some yield curve object
    spot_prices={"STOCK_XYZ": 100.0}
)

# 2. Instrument: down-and-in call
down_in_call = BarrierOption(
    strike=110,
    maturity=1.0,
    option_type="call",
    barrier_level=80,
    barrier_type="down-and-in",
    rebate=0.0
)

# 3. Pricing engine
bs_engine = BlackScholesEngine(
    interest_rate=0.02,
    volatility=0.20,
    spot_price=market.get_spot_price("STOCK_XYZ")
)

# 4. Valuation
valuation_req = ValuationRequest(instrument=down_in_call, pricer=bs_engine, market=market)
fair_value = valuation_req.run_valuation()

print("The down-and-in call fair value:", fair_value)
```

---

## Key Modules

### `src/instruments`
- **`instrument_base.py`**: Abstract base class for all instruments.  
- **`vanilla_option.py`**: Vanilla option definitions (call/put, European style).  
- **`barrier_option.py`**: Extensions of `VanillaOption` for barrier structures.  
- **`fx_option.py`**: FX barrier option specifics (domestic/foreign currency).  
- **`variance_swaption.py`**: A hypothetical variance swaption instrument.  

### `src/market_data/market.py`
- **`Market`** class for holding all necessary market data like spot prices, yield curves, and volatility surfaces.

### `src/utils`
- **`black_scholes_functions.py`**: Analytical formula components for BS model.  
- **`monte_carlo_functions.py`**: Monte Carlo path simulation and payoff evaluation.  
- **`pde_functions.py`**: Finite difference approaches to solve the BS PDE.

### `src/models`
- **`pricing_engine_base.py`**: Abstract pricing engine interface.  
- **`black_scholes/black_scholes_pricing.py`**: Black–Scholes model-based engine.  
- **`monte_carlo/monte_carlo_pricing.py`**: Monte Carlo-based engine.  
- **`pde/pde_pricing.py`**: PDE-based engine.

### `src/valuation`
- **`valuation_request.py`**: Ties together an `Instrument` and a `PricingEngine` with `Market` data to compute value.  
- **`valuation_result.py`**: Stores the output (fair value, greeks, scenario results, etc.).

### `examples`
- **`barrier_option_pricing.ipynb`**: Demo for barrier options using BS, MC, and PDE methods.  
- **`vanilla_option_pricing_ipynb`**: Demo for vanilla options using the three pricing engines.  
- **`variance_swap_swaption_pricing.ipynb`**: Demo for variance swap swaptions (illustrative only).

---

## Contributing

Contributions are welcome! If you’d like to:
1. Report a bug  
2. Submit a feature request  
3. Improve documentation  

Please open an [issue](https://github.com/YourUserName/barrier-options-pricing/issues) or a [pull request](https://github.com/YourUserName/barrier-options-pricing/pulls).
