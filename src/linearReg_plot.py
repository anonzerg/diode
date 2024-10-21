import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e as e  # elementary charge     (C)
from scipy.constants import k as k  # boltzmann's constant  (J/K)
from scipy.constants import h as h  # planck's constant     (J.s)
from scipy.constants import c as c  # speed of light        (m/s)

# TODO: check for units

# prompt to take temperature in kelvin
temp = float(input("input temperature: "))

# prompt to take LED color
color = input("input LED color (if not LED input 'none'): ")
# LED wavelength in nanometers
colors = {"red": 630, "green": 532, "blue": 465, "none": 0}
if color not in colors.keys():
    print("\ninvalid color for LED!")
    color = input("input LED color (if not LED input 'none'): ")
else:
    wavelength = colors[color]
    if color != "none":
        print(f"{color} LED with {wavelength}nm wavelength")

# read data from file and save to numpy array
data = np.loadtxt("./data/data.txt", delimiter=" ", usecols=(0, 1))

print(data)

# save 1st column as voltage and 2nd column as current
voltage = data[:, 0]
current = data[:, 1]
# coefficients = np.polyfit(voltage, current, 1)
# slope, intercept = coefficients

# TODO: check for NaN, NULL in data
# plot voltage-current graph of diode
plt.figure(1)
plt.plot(voltage, current, "*", label="data points")
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
n = 2;
boltzmann_constant = (e / (n * temp)) * (1 / slope)
boltzmann_constant_error = (abs(k - boltzmann_constant) / k) * 100

if wavelength:
    planck_constant = (wavelength * e * voltage) / c
else:
    print("no LED no planck constant!")

planck_constant_error = (abs(h - planck_constant) / h) * 100

print("="*80)
print(f"boltzmann constant: {boltzmann_constant}")
print(f"relative error: {boltzmann_constant_error}%")

print("="*80)
print(f"planck constant: {planck_constant}")
print(f"relative error: {planck_constant_error}%")

