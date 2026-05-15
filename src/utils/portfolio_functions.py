import numpy as np


def portfolio_return(return_np, weight_np):
    return np.dot(return_np, weight_np)


def index_returns(return_np, base_value=100):
    """Convert periodic returns into a cumulative total return index."""
    return (return_np + 1).cumprod() * base_value
