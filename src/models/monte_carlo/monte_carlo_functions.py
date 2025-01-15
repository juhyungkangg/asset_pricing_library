# src/utils/monte_carlo_functions.py
import numpy as np
from tqdm import tqdm
from scipy.integrate import trapezoid
from scipy.stats import norm

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


def variance_swap_swaption_price_mc(var_swap_spot, K, r, T1, T2, params, n_paths, n_steps):
    nu, theta, k1, k2, rho = params['nu'], params['theta'], params['k1'], params['k2'], params['rho']

    dt = T1 / n_steps

    dW_t_1 = np.random.normal(loc=0, scale=np.sqrt(dt), size=(n_paths, n_steps))
    dB_t   = np.random.normal(loc=0, scale=np.sqrt(dt), size=(n_paths, n_steps))
    dW_t_2 = rho * dW_t_1 + np.sqrt(1 - rho**2) * dB_t

    def xi_t_u_func(u):
        # Instantaneous VS Forward variances
        xi_t_u = np.zeros((n_paths, n_steps + 1)) # t: 0 ~ T1 and u: T1 ~ T2
        xi_t_u[:, 0] = var_swap_spot # xi_0_u = 0.2 by the given condition for any u

        alpha_theta = 1 / np.sqrt((1 - theta)**2 + theta**2 + 2 * rho * theta * (1-theta))

        for i in range(1, xi_t_u.shape[1]):
            xi_t_u[:, i] = xi_t_u[:, i-1] + (2 * nu) * xi_t_u[:, i-1] * alpha_theta *\
                         ((1 - theta) * np.exp(-k1 * (u - dt * (i-1))) * dW_t_1[:, i-1]\
                             + theta  * np.exp(-k2 * (u - dt * (i-1))) * dW_t_2[:, i-1])

        return xi_t_u[:, -1]

    # Calculate the integral
    integral_steps = 1000
    u_val = np.linspace(T1, T2, integral_steps)
    xi_val = np.zeros((n_paths, integral_steps))

    for i in tqdm(range(integral_steps)):
        xi_val[:, i] = xi_t_u_func(u_val[i])

    integral_val = np.zeros(n_paths)

    for i in tqdm(range(n_paths)):
        integral_val[i] = trapezoid(xi_val[i], x=u_val)

    # Payoff
    payoff = np.maximum(integral_val / (T2 - T1) - K, 0)

    # Price
    discount_factor = np.exp(-r * T1)
    price = np.mean(payoff * discount_factor)

    return price




if __name__ == '__main__':
    # Set variables
    T1, T2 = 0.5, 1.0
    r = 0.01  # Flat discount rate
    var_swap_spot = 0.2
    strike = var_swap_spot  # ATM
    params = [
        {'nu': 1.50, 'theta': 0.312, 'k1': 2.63, 'k2': 0.42, 'rho': -0.7},
        {'nu': 1.74, 'theta': 0.245, 'k1': 5.35, 'k2': 0.28, 'rho': 0.0},
        {'nu': 1.86, 'theta': 0.230, 'k1': 7.54, 'k2': 0.24, 'rho': 0.7}
    ]

    print(variance_swap_swaption_price_mc(var_swap_spot=var_swap_spot, K=var_swap_spot, r=r, T1=T1, T2=T2, params=params[0], n_paths=100000, n_steps=252))

