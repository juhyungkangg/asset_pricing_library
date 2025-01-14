# src/utils/pde_functions.py
import numpy as np

import numpy as np

import numpy as np


def option_price_pde(
        S0: float, K: float, T: float, r: float,
        sigma: float, option_type: str,
        nx: int, nt: int,
        x_max: float, x_min: float,
        ):
    """
    Price a European call or put option using a finite difference method
    for the Black–Scholes PDE on [0, x_max].
    """
    # Create spatial and time steps
    dx = x_max / nx
    dt = T / nt

    # Discretize asset prices
    x = np.linspace(x_min, x_max, nx + 1)

    # Terminal payoff for call/put
    V = np.zeros_like(x)
    if option_type == 'call':
        V = np.maximum(x - K, 0)
    elif option_type == 'put':
        V = np.maximum(K - x, 0)

    # Initialize tridiagonal matrix for implicit scheme
    M = np.zeros((nx + 1, nx + 1))
    M[0, 0] = 1
    M[-1, -1] = 1

    # Coefficients for the PDE discretization
    alpha = -dt * (r * x / (2 * dx) + (sigma ** 2) * (x ** 2) / (2 * (dx ** 2)))
    beta = 1 + r * dt + (sigma ** 2) * dt / (dx ** 2) * (x ** 2)
    gamma = -dt * (-r * x / (2 * dx) + (sigma ** 2) * (x ** 2) / (2 * (dx ** 2)))

    # Fill sub-, main-, super-diagonal
    np.fill_diagonal(M[1:-1, 2:], alpha[1:])
    np.fill_diagonal(M[1:-1, 1:], beta[1:])
    np.fill_diagonal(M[1:-1, 0:], gamma[1:])

    # Backward time stepping
    t = 0
    for i in range(nt, 0, -1):
        # Boundary condition vector for each step
        C = np.append(
            np.zeros(nx),
            np.exp(-r * (T - t + dt)) * K - np.exp(-r * (T - t)) * K
        )
        t -= dt

        # Solve for the new option values
        V = np.linalg.inv(M) @ V + C

    # Find the grid index closest to S0
    x_idx = np.argmin(np.abs(x - S0))
    # Return price at that grid point
    return V[x_idx]

def vanilla_option_price_pde(
        S0: float, K: float, T: float, r: float,
        sigma: float, option_type: str,
        x_max: float,
        nx: int = 300, nt: int = 300,
        ):
    return option_price_pde(
        S0=S0, K=K, T=T, r=r,
        sigma=sigma, option_type=option_type,
        x_max=x_max, x_min=0, nx=nx, nt=nt)

def barrier_option_price_pde(
        S0: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        B: float,
        option_type: str,
        barrier_type: str,
        nx: int = 300,
        nt: int = 300,
        ):
    """
    Price a European call or put option using a finite difference method
    for the Black–Scholes PDE on [0, x_max].
    """


    # Discretize asset prices
    x_max = 0
    if barrier_type.lower().startswith('up'):
        if barrier_type.lower().endswith('in'):
            x_max = S0 * 3
            x = np.linspace(B, x_max, nx + 1)
        elif barrier_type.lower().endswith('out'):
            pass
    elif barrier_type.lower().startswith('down'):
        if barrier_type.lower().endswith('in'):
            pass
        elif barrier_type.lower().endswith('out'):
            pass

    # Create spatial and time steps
    dx = x_max / nx
    dt = T / nt

    # Terminal payoff for call/put
    V = np.zeros_like(x)
    if option_type == 'call':
        V = np.maximum(x - K, 0)
    elif option_type == 'put':
        V = np.maximum(K - x, 0)

    # Initialize tridiagonal matrix for implicit scheme
    M = np.zeros((nx + 1, nx + 1))
    M[0, 0] = 1
    M[-1, -1] = 1

    # Coefficients for the PDE discretization
    alpha = -dt * (r * x / (2 * dx) + (sigma ** 2) * (x ** 2) / (2 * (dx ** 2)))
    beta = 1 + r * dt + (sigma ** 2) * dt / (dx ** 2) * (x ** 2)
    gamma = -dt * (-r * x / (2 * dx) + (sigma ** 2) * (x ** 2) / (2 * (dx ** 2)))

    # Fill sub-, main-, super-diagonal
    np.fill_diagonal(M[1:-1, 2:], alpha[1:])
    np.fill_diagonal(M[1:-1, 1:], beta[1:])
    np.fill_diagonal(M[1:-1, 0:], gamma[1:])

    # Backward time stepping
    t = 0
    for i in range(nt, 0, -1):
        # Boundary condition vector for each step
        C = np.append(
            np.zeros(nx),
            np.exp(-r * (T - t + dt)) * K - np.exp(-r * (T - t)) * K
        )
        t -= dt

        # Solve for the new option values
        V = np.linalg.inv(M) @ V + C

    # Find the grid index closest to S0
    x_idx = np.argmin(np.abs(x - S0))
    # Return price at that grid point
    return V[x_idx]



if __name__ == "__main__":
    S0 = 100.
    K = 100.
    T = 1.
    r = 0.05
    sigma = 0.2
    option_type = 'call'
    x_max = 100. * 3
    nx = 300
    nt = 300

    price = vanilla_option_price_pde(S0, K, T, r, sigma, option_type, x_max, nx, nt)
    print(price)
