import math
import numpy as np
from scipy.optimize import curve_fit

def load_data(file_path: str) -> list[float]:
    """ read data from text file. """

    data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                voltage, current = map(float, line.split())
                if voltage == 0.0 or current == 0.0:
                    continue
                else:
                    data.append([voltage, current])
            except ValueError:
                continue

    return data

def lin_model(x: float, slope: float, intercept: float) -> float:
    return (slope * x + intercept)

# https://en.wikipedia.org/wiki/Coefficient_of_determination
def coefficient_of_determination(x_vec: list[float], y_vec: list[float]) -> float:
    """ provides a measure of how well observed outcomes are replicated by the model. """

    parameters, covariance = curve_fit(lin_model, x_vec, y_vec)
    slope, intercept = parameters
    y_pred = []
    for elm in x_vec:
        y_pred.append(lin_model(elm, slope, intercept))

    y_pred = np.array(y_pred)
    y_mean = np.mean(y_vec)
    residual = np.subtract(y_vec, y_pred)

    sum_of_square_residual = np.sum(np.square(residual))
    sum_of_square_total = np.sum(y_vec - y_mean)
    if sum_of_square_total == 0:
        return float("nan")
    r2 = 1.0 - (sum_of_square_residual / sum_of_square_total)
    return r2


def sliding_window(x_vec: list[float], y_vec: list[float], window_size: int) -> tuple[float, float]:
    """ separate linear portion of data using sliding window algorithm. """
    best_r2 = -np.inf
    best_start = 0
    n = x_vec.size
    
    parameters, covariance = curve_fit(lin_model, x_vec, y_vec)
    slope, intercept = parameters
    for i in range(n - window_size + 1):
        x_window = [i, i + window_size]
        y_window = [i, i + window_size]
        y_pred = []
        for elm in x_window:
            y_pred.append(lin_model(elm, slope, intercept))

        y_pred = np.array(y_pred)
    r2 = coefficient_of_determination(y_window, y_pred)
    if math.isnan(r2):
        return (None, None)
    print(r2)
    if r2 > best_r2:
        best_r2 = r2
        best_start = i
    end = best_start + window_size
    return (best_start, end)

