import numpy as np
import matplotlib.pyplot as plt
#                                     physical constant name    | unit
#                                     --------------------------------
from scipy.constants import e as e  # elementary charge         | C
from scipy.constants import k as k  # boltzmann's constant      | J/K
from scipy.constants import h as h  # planck's constant         | J.s
from scipy.constants import c as c  # speed of light            | m/s

def load_data(file_path):
    """ read data from text file. """

    data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                voltage, current = map(float, line.split())
                data.append([voltage, current])
            except ValueError:
                continue

    return data

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
            if color != "none":
                print(f"[!] {color.capitalize()} LED with {wavelength * 1e9}nm wavelength")

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

        # plot voltage-current graph of diode
        plt.figure(1)
        plt.plot(voltage, current, "*", label = "data points")
        # plt.plot(voltage, slope * voltage + intercept, color="red", label="fitted line")
        plt.xlabel("voltage (V)")
        plt.ylabel("current (mA)")
        plt.title("I-V characteristic of diode")
        plt.legend()
        plt.show()

        # plot log-scale of I-V graph
        plt.figure(2)
        plt.plot(voltage, np.log(current), "+")
        plt.xlabel("voltage (V)")
        plt.ylabel("current (mA) (log scale)")
        plt.title("logarithmic plot of I-V")
        plt.show()

        # fit log-scale current
        log_current = np.log(current)
        coefficients = np.polyfit(voltage, log_current, 1)
        slope, intercept = coefficients

        # find boltzmann constant from slope
        # https://en.wikipedia.org/wiki/Diode_modelling
        n = colors_ideality[color][1] # ideality
        print(n)
        boltzmann_constant = (e / (n * temp)) * (1 / slope)
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

