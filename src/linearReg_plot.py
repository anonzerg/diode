import numpy as np
import matplotlib.pyplot as plt
#                                     physical constant name    | unit
#                                     --------------------------------
from scipy.constants import e as e  # elementary charge         | C
from scipy.constants import k as k  # boltzmann's constant      | J/K
from scipy.constants import h as h  # planck's constant         | J.s
from scipy.constants import c as c  # speed of light            | m/s
from scipy.optimize import curve_fit

def load_data(file_path):
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

# https://en.wikipedia.org/wiki/Coefficient_of_determination
def coefficient_of_determination(x_vec, y_vec):
    """ provides a measure of how well observed outcomes are replicated by the model. """
    def lin_model(x, slope, intercept):
        y = slope * x + intercept
        return y

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
    r2 = 1.0 - (sum_of_square_residual / sum_of_square_total)
    return r2


def sliding_window(x_vec, y_vec, window_size):
    """ separate linear portion of data using sliding window algorithm. """
    best_r2 = -np.inf
    best_start = 0
    n = x_vec.size
    def lin_model(x, slope, intercept):
        y = slope * x + intercept
        return y
    
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
    print(r2)
    if r2 > best_r2:
        best_r2 = r2
        best_start = i
    end = best_start + window_size
    return best_start, end

def main():
    try:
        # prompt to take temperature in kelvin
        temp = float(input("input temperature (in kelvin): "))

        # prompt to take LED color
        color = input("input LED color (if not LED input 'none'): ").lower()
        # LED wavelength in nanometers
        colors_ideality = {"red": [630e-9, 1.5], "green": [532e-9, 1.98], "blue": [465e-9, 1.56], "none": [0, 2.0]}
        if color not in colors_ideality.keys():
            raise ValueError("\n[-] invalid color for LED!")
        else:
            wavelength = colors_ideality[color][0]
            n = colors_ideality[color][1] # ideality
            
            if color != "none":
                print(f"[!] {color.capitalize()} LED with {wavelength * 1e9}nm wavelength and ideality of {n}.")

        # read data from file and save to numpy array
        data = load_data("./data/data.txt")
        if not data:
            print("[-] failed to load data or data is empty.")
            exit()

        data = np.array(data)
        # save 1st column as voltage and 2nd column as current
        voltage = data[:, 0]
        current = data[:, 1]

        # check for NaN, NULL in data
        if np.isnan(data).any():
            raise ValueError("\n[-] data contains NaN values.")

        # fit log-scale current
        log_current = np.log(current)
        #coefficients = np.polyfit(voltage, log_current, 1)
        #slope, intercept = coefficients
        
        # number of data point selected from linear portion of data
        window_size = 40
        start, end = sliding_window(voltage, log_current, window_size)
        def func(voltage, slope, intercept):
            current = slope * voltage + intercept
            return current

        parameters, covariance = curve_fit(func, voltage[start: end], log_current[start: end])
        slope, intercept = parameters
        standard_error = np.sqrt(np.diag(covariance))
        standard_error_slope = standard_error[0]
        standard_error_intercept = standard_error[1]

        print(f"[!] value of slope is {slope:.4f} with standard error of {standard_error_slope:.4f}.")
        print(f"[!] value of intercept is {intercept:.4f} with standard error of {standard_error_intercept:.4f}.")

        # plot voltage-current graph of diode
        plt.figure(1)
        plt.plot(voltage, current, "*", label = "data points")
        #plt.plot(voltage, slope * voltage + intercept, color="red", label="fitted line")
        #plt.plot(voltage, func(voltage, slope, intercept), color = "red", label = "fitted line")
        plt.xlabel("voltage (V)")
        plt.ylabel("current (mA)")
        plt.title("I-V characteristic of diode")
        plt.legend()
        plt.show()

        # plot log-scale of I-V graph
        plt.figure(2)
        plt.plot(voltage, np.log(current), "+")
        #plt.plot(voltage, slope * voltage + intercept, color="red", label="fitted line")
        plt.plot(voltage, func(voltage, slope, intercept), color = "red", label = "fitted line data")
        plt.scatter(voltage[start: end], log_current[start: end], color = "green", label = "linear")
        plt.xlabel("voltage (V)")
        plt.ylabel("current (mA) (log scale)")
        plt.title("logarithmic plot of I-V")
        plt.show()

        # find boltzmann constant from slope
        # https://en.wikipedia.org/wiki/Diode_modelling
        boltzmann_constant = (e / (n * temp * 2.3)) * (1 / slope)
        boltzmann_constant_error = (abs(k - boltzmann_constant) / k) * 100

        if wavelength != 0:
            planck_constant = (wavelength * e * np.mean(voltage)) / c
            planck_constant_error = (abs(h - planck_constant) / h) * 100
        else:
            planck_constant = None
            planck_constant_error = None

        print("="*80)
        print(f"[!] boltzmann constant: {boltzmann_constant:.4e} J/K")
        print(f"[!] relative error: {boltzmann_constant_error:.2f} %")

        if planck_constant is not None:
            print("="*80)
            print(f"[!] planck constant: {planck_constant:.4e}")
            print(f"[!] relative error: {planck_constant_error:.2f} %")
        else:
            print("[!] no LED, so no planck constant can be calculated.")

    except Exception as error:
        print(f"[-] an error occurred: {error}")

if __name__ == "__main__":
    main()

