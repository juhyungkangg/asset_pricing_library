# src/utils/black_scholes_functions.py
import math
from math import exp, sqrt, log
from scipy.stats import norm

def d1(S, K, T, r, q, sigma):
    return (log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*sqrt(T))

def d2(S, K, T, r, q, sigma):
    return d1(S, K, T, r, q, sigma) - sigma*sqrt(T)

def vanilla_option_price_bs(S: float, K: float, T: float, r: float, q: float, sigma: float, option_type: str) -> float:
    _d1 = d1(S, K, T, r, q, sigma)
    _d2 = _d1 - sigma*sqrt(T)

    if option_type.lower() == "call":
        return S * exp(-q * T) * norm.cdf(_d1) - K * exp(-r * T) * norm.cdf(_d2)
    elif option_type.lower() == "put":
        return K*exp(-r*T)*norm.cdf(-_d2) - S*exp(-q*T)*norm.cdf(-_d1)
    else:
        raise ValueError("Option type must be either 'call' or 'put'")

def lmbda(r, q, sigma):
    return (r - q) / sigma**2 - 1 / 2

def S_tilde(S, B):
    return B**2 / S

def barrier_option_price_bs(S: float, K: float, T: float, r: float, q: float, sigma: float, B: float, option_type: str,
                            barrier_type: str) -> float:
    v1 = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
    v2 = vanilla_option_price_bs(S_tilde(S, B), K, T, r, q, sigma, option_type)

    l = lmbda(r, q, sigma)

    if barrier_type.lower().startswith("up"):
        exponent = 2 * (1 + l)
    elif barrier_type.lower().startswith("down"):
        exponent = 2 * (1 - l)
    else:
        raise "Cannot recognise barrier type '{}'".format(option_type)

    if barrier_type.lower().endswith("in"):
        price = (B / S)**exponent * v2
    elif barrier_type.lower().endswith("out"):
        price = v1 - (B / S)**exponent * v2
    else:
        raise "Cannot recognise barrier type '{}'".format(barrier_type)

    return price


if __name__ == "__main__":
    pass
