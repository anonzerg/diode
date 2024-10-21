# Asst. Prof. Majtaba Nasiri
# BSPhy. M. Mahdi Farrokhi
# Nov 20, 2023

import subprocess

if __name__ == "__main__":

    print()
    print("program to find boltzmann's constant and planck's constant using arduino board.")
    print("authors:")
    print("\tAsst. Prof. Majtaba Nasiri\n\tBSPhy. M. Mahdi Farrokhi\n")
    print("=" * 80)
    print("gathering data and writing to ./data/data.txt file...")
    print("=" * 80)
    subprocess.run(["python", "./src/find_serial.py"])

    print()
    print("=" * 80)
    print("processing data and creating plot...")
    print("=" * 80)
    subprocess.run(["python", "./src/linearReg_plot.py"])
