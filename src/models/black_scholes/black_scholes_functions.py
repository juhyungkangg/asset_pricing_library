# src/utils/black_scholes_functions.py
import math
from math import exp, sqrt, log
from scipy.stats import norm
import numpy as np

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

def alpha(r, q, sigma):
    return (1 - (r - q) / (sigma**2 / 2)) / 2

def S_tilde(S, B):
    return B**2 / S

def barrier_option_price_bs(S: float, K: float, T: float, r: float, q: float, sigma: float, B: float, option_type: str,
                            barrier_type: str) -> float:
    a = alpha(r, q, sigma)

    if option_type.lower() == "call":
        if barrier_type.lower().startswith("down"):
            if B <= K:
                call_1 = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
                call_2 = vanilla_option_price_bs(S_tilde(S, B), K, T, r, q, sigma, option_type)

                out_option = call_1 - (S / B)**(2 * a) * call_2

                if barrier_type.lower().endswith("in"):
                    return call_1 - out_option
                elif barrier_type.lower().endswith("out"):
                    return out_option
            elif B > K:
                vanilla_call = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
                call_1 = vanilla_option_price_bs(S, B, T, r, q, sigma, option_type)
                call_2 = vanilla_option_price_bs(S_tilde(S, B), B, T, r, q, sigma, option_type)
                d2_1 = d2(S, B, T, r, q, sigma)
                digital_call_1 = np.exp(-r * T) * norm.cdf(d2_1)
                d2_2 = d2(S_tilde(S, B), B, T, r, q, sigma)
                digital_call_2 = np.exp(-r * T) * norm.cdf(d2_2)

                out_option = call_1 + (B - K) * digital_call_1 - (S / B) ** (2 * a) * (call_2 + (B - K) * digital_call_2)

                if barrier_type.lower().endswith("in"):
                    return vanilla_call - out_option
                elif barrier_type.lower().endswith("out"):
                    return out_option
        elif barrier_type.lower().startswith("up"):
            if B <= K:
                raise ValueError("The price of the up-and-out barrier call option vanishes when B <= K.")
            elif B > K:
                # line 1
                vanilla_call = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
                d1_1 = d1(S, B, T, r, q, sigma)
                line1 = vanilla_call - S * norm.cdf(d1_1)

                # line 2
                d1_2 = d1(B**2, K * S, T, r, q, sigma)
                d1_3 = d1(B, S, T, r, q, sigma)
                line2 = -B * (B / S)**(2 * r / sigma**2) * (norm.cdf(d1_2) - norm.cdf(d1_3))

                # line 3
                d2_1 = d2(S, B, T, r, q, sigma)
                line3 = np.exp(-r * T) * K * norm.cdf(d2_1)

                # line 4
                d2_2 = d2(B**2, K * S, T, r, q, sigma)
                d2_3 = d2(B, S, T, r, q, sigma)
                line4 = np.exp(-r * T) * K * (S / B)**(1 - 2 * r / sigma**2) * (norm.cdf(d2_2) - norm.cdf(d2_3))

                out_option = line1 + line2 + line3 + line4


                if barrier_type.lower().endswith("in"):
                    return vanilla_call - out_option
                elif barrier_type.lower().endswith("out"):
                    return out_option
    elif option_type.lower() == "put":
        if barrier_type.lower().startswith("down"):
            if B <= K:
                # line 1
                vanilla_put = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
                d1_1 = d1(S, B, T, r, q, sigma)
                line1 = vanilla_put + S * norm.cdf(-d1_1)

                # line 2
                d1_2 = d1(B**2, K * S, T, r, q, sigma)
                d1_3 = d1(B, S, T, r, q, sigma)
                line2 = -B * (B / S)**(2 * r / sigma**2) * (norm.cdf(d1_2) - norm.cdf(d1_3))

                # line 3
                d2_1 = d2(S, B, T, r, q, sigma)
                line3 = -np.exp(-r * T) * K * norm.cdf(-d2_1)

                # line 4
                d2_2 = d2(B**2, K * S, T, r, q, sigma)
                d2_3 = d2(B, S, T, r, q, sigma)
                line4 = np.exp(-r * T) * K * (S / B)**(1 - 2 * r / sigma**2) * (norm.cdf(d2_2) - norm.cdf(d2_3))

                out_option = line1 + line2 + line3 + line4

                if barrier_type.lower().endswith("in"):
                    return vanilla_put - out_option
                elif barrier_type.lower().endswith("out"):
                    return out_option
            elif B > K:
                raise ValueError("B cannot be larger than K for down-and-in/out barrier put option.")
        elif barrier_type.lower().startswith("up"):
            if B <= K:
                vanilla_put = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
                put_1 = vanilla_option_price_bs(S, B, T, r, q, sigma, option_type)
                put_2 = vanilla_option_price_bs(S_tilde(S, B), K, T, r, q, sigma, option_type)
                d2_1 = d2(S, B, T, r, q, sigma)
                digital_put_1 = np.exp(-r * T) * norm.cdf(-d2_1)
                d2_2 = d2(S_tilde(S, B), B, T, r, q, sigma)
                digital_put_2 = np.exp(-r * T) * norm.cdf(-d2_2)

                out_option = put_1 + (K - B) * digital_put_1 - (S / B) ** (2 * a) * (put_2 + (K - B) * digital_put_2)

                if barrier_type.lower().endswith("in"):
                    return vanilla_put - out_option
                elif barrier_type.lower().endswith("out"):
                    return out_option
            elif B > K:
                put_1 = vanilla_option_price_bs(S, K, T, r, q, sigma, option_type)
                put_2 = vanilla_option_price_bs(S_tilde(S, B), K, T, r, q, sigma, option_type)

                out_option = put_1 - (S / B)**(2 * a) * put_2

                if barrier_type.lower().endswith("in"):
                    return put_1 - out_option
                elif barrier_type.lower().endswith("out"):
                    return out_option


if __name__ == "__main__":
    option_price = barrier_option_price_bs(100, 90, 1, 0.02, 0.0, 0.2, 120, "call", "up-and-out")
