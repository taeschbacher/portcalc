import numpy as np


def portfolio_return(return_np, weight_np):
    return np.dot(return_np, weight_np)
