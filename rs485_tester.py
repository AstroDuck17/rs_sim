import random
import sys
from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from threading import Thread
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

# create data context
def create_context(values):
    return ModbusServerContext(
        slaves=ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, values)
        ),
        single=True
    )

def run_modbus_server(context):
    StartSerialServer(context, port="/dev/ttyUSB0", baudrate=9600, parity='N', stopbits=1, bytesize=8)

def display_values(label, values):
    print(f"\n--- {label} ---")
    print(f"Voltage: {values[0] / 10.0:.1f} V")
    print(f"Frequency: {values[1] / 10.0:.1f} Hz")
    print(f"Current: {values[2] / 10.0:.1f} A")
    print(f"Active Power: {values[3] / 10.0:.1f} kW\n\n")

def fixed_values():
    values = [2200, 1200, 500, 1150]  # 220.0V, 120.0Hz, 5.0A, 1.10kW
    display_values("Fixed Values", values)
    context = create_context(values)
    run_modbus_server(context)

def random_values():
    values = [
        random.randint(2000, 3000),  # Voltage: 200V–300V
        random.randint(400, 600),    # Frequency: 40.0–60.0 Hz
        random.randint(100, 1500),   # Current: 1A–15A
        random.randint(100, 5000)    # Power: 0.1–5.0kW
    ]
    display_values("Random Generated Values", values)
    context = create_context(values)
    run_modbus_server(context)

def abnormal_values():
    values = [0, 0, 9999, -500]  # 0V, 0Hz, 999.9A, -500W
    display_values("Abnormal values", values)
    context = create_context(values)
    run_modbus_server(context)

def main_menu():
    while True:
        print("\nRS-485 Energy Meter Tester")
        print("1. Fixed Value Mode")
        print("2. Random Value Mode")
        print("3. Abnormal Values Mode")
        print("4. Exit")

        choice = input("Choose mode: ")

        if choice == '1':
            fixed_values()
        elif choice == '2':
            random_values()
        elif choice == '3':
            abnormal_values()
        elif choice == '4':
            print("Exiting tester.")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
