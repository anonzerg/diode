# Asst. Prof. Majtaba Nasiri
# BSPhy. M. Mahdi Farrokhi
# Nov 20, 2023

import serial
import time
import serial.tools.list_ports
import os


def find_serial_port():
    """ automatically find connected arduino ports. """

    # search for all serial ports. if description match "Arduino", add them to list.
    serial_ports = [port.device for port in serial.tools.list_ports.comports() if "Arduino" in port.description]
    if serial_ports:
        print(f"[+] connected to {serial_ports[0]}")
        return serial_ports[0]
    else:
        raise IOError("[-] arduino board not found!")

def read_save_serial_data(port, baud_rate, output_path, duration):
    """ read data from serial port and write them to a text file. """

    # ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok = True)

    try:
        # open serial port and file path
        with serial.Serial(port, baud_rate, timeout = 1) as ser, open(output_path, "w") as output_file:

            # set init time
            start_time = time.time()
            
            # read data until the duration runs out
            while time.time() - start_time < duration:

                # check if serial is free
                if ser.in_waiting > 0:

                # read data from serial
                    data = ser.readline().decode("utf-8", errors = "ignore").strip()
                    print(data)

                    # write data to file
                    output_file.write(data + "\n")
    except serial.SerialException as error:
        print(f"[-] serial exception: {e}")
    except IOError as error:
        print(f"[-] I/O error: {error}")
    except Exception as error:
        print(f"[-] unexpected error: {error}")

if __name__ == "__main__":
    try:
        serial_port = find_serial_port()
        baud_rate = 9600
        output_path = "./data/data.txt"
        duration = int(input("input data gathering duration is seconds: "))

        read_save_serial_data(serial_port, baud_rate, output_path, duration)
    except Exception as error:
        print(f"{error}")

