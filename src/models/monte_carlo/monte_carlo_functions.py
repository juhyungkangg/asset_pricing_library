# src/utils/monte_carlo_functions.py
import numpy as np


def simulate_paths_gbm(n_paths: int, n_steps: int, T: float, r: float, q: float, sigma: float, S0: float) -> np.ndarray:
    """
    Simulate paths for a Geometric Brownian Motion under the risk-neutral measure,
    using a log-Euler scheme for efficiency.

    Parameters
    ----------
    n_paths : int
        Number of Monte Carlo paths to simulate.
    n_steps : int
        Number of discrete time steps per path.
    T : float
        Time to maturity (in years).

    Returns
    -------
    paths : np.ndarray
        A 2D array of shape (n_paths, n_steps+1). Each row is one simulated path
        from t=0 to t=T. paths[:,0] = S0.
    """
    dt = T / n_steps
    # Random draws for the increments: shape (n_paths, n_steps)
    z = np.random.normal(size=(n_paths, n_steps))

    # (r - q - 0.5*sigma^2)*dt + sigma*sqrt(dt)*z
    drift = (r - q - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt)

    # Cumulative sum of log-increments
    log_increments = drift + diffusion * z
    log_paths = np.cumsum(log_increments, axis=1)

    # Prepend a column of zeros for the initial log(S0)
    # so that at t=0, log(S) = log(S0)
    log_paths = np.hstack((np.zeros((n_paths, 1)), log_paths))

    # Exponentiate and multiply by S0 to get price paths
    paths = S0 * np.exp(log_paths)
    return paths


def vanilla_option_price_mc(paths: np.ndarray, strike: float, maturity: float, interest_rate: float, option_type: str) -> float:
    S_T = paths[:, -1] # terminal prices

    if option_type.lower() == "call":
        return np.mean(np.maximum(S_T - strike, 0.0)) * np.exp(-interest_rate * maturity)
    elif option_type.lower() == "put":
        return np.mean(np.maximum(strike - S_T, 0.0)) * np.exp(-interest_rate * maturity)
    else:
        raise "Cannot recognise option type '{}'".format(option_type)

def barrier_option_price_mc(paths: np.ndarray, strike: float, maturity: float, interest_rate: float, barrier_level: float,
                            rebate: float, option_type: str, barrier_type: str) -> float:
    S_T = paths[:, -1] # terminal prices

    if option_type.lower() == "call":
        vanilla_prices = np.maximum(S_T - strike, 0.0) * np.exp(-interest_rate * maturity)
    elif option_type.lower() == "put":
        vanilla_prices = np.maximum(strike - S_T, 0.0) * np.exp(-interest_rate * maturity)
    else:
        raise "Cannot recognise option type '{}'".format(option_type)

    if barrier_type.lower().startswith("up"):
        barrier_hit = np.any(paths >= barrier_level, axis=1)
    elif barrier_type.lower().startswith("down"):
        barrier_hit = np.any(paths <= barrier_level, axis=1)
    else:
        raise "Cannot recognise barrier type '{}'".format(option_type)

    if barrier_type.lower().endswith("in"):
        payoff = np.where(barrier_hit, vanilla_prices, rebate)
    elif barrier_type.lower().endswith("out"):
        payoff = np.where(~barrier_hit, vanilla_prices, rebate)
    else:
        raise "Cannot recognise barrier type '{}'".format(barrier_type)

    return float(np.mean(payoff))







if __name__ == '__main__':
    pass
