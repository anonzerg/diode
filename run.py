# Mojtaba Nasiri
# Mahdi Farrokhi
# rewrite Jan 14, 2025

import matplotlib.pyplot as plt
#                                     physical constant name    | unit
#                                     --------------------------------
from scipy.constants import e as e  # elementary charge         | C
from scipy.constants import k as k  # boltzmann's constant      | J/K
from scipy.constants import h as h  # planck's constant         | J.s
from scipy.constants import c as c  # speed of light            | m/s

from util.find_serial import find_serial_port, read_save_serial_data
from util.linearReg import load_data, sliding_window

flag ="""

+-----------------------------------------------+
|   program to find boltzmann's constant and    |
|   planck's constant from diode and LED using  |
|   Arduino board.                              |
|                                               |
|   Authors: Mojtaba Nasisri                    |
|            Mahdi Farrokhi                     |
+-----------------------------------------------+

"""

def main():
    print(flag)

    try:
        serial_port = find_serial_port()
        baud_rate = 9600
        output_path = "./data/data.txt"
        duration = int(input("input data gathering duration is seconds: "))

        read_save_serial_data(serial_port, baud_rate, output_path, duration)
    except Exception as error:
        print(f"{error}")
        exit(1)


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
            exit(1)

        data = np.array(data)
        # save 1st column as voltage and 2nd column as current
        voltage = data[:, 0]
        current = data[:, 1]

        # check for NaN, NULL in data
        if np.isnan(data).any():
            raise ValueError("\n[-] data contains NaN values.")

        # fit log-scale current
        log_current = np.log(current)
        
        # number of data point selected from linear portion of data
        window_size = 40
        (start, end) = sliding_window(voltage, log_current, window_size)
        if (start == None) or (end == None):
            print("[-] sliding_window failed.")
            exit(1)

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
        plt.xlabel("voltage (V)")
        plt.ylabel("current (mA)")
        plt.title("I-V characteristic of diode")
        plt.legend()
        plt.show()

        # plot log-scale of I-V graph
        plt.figure(2)
        plt.plot(voltage, np.log(current), "+")
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

