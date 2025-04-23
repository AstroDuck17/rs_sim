import sys
import random
import minimalmodbus
import serial

PORT        = '/dev/ttyUSB0'   # your USB→RS-485 adapter device
SLAVE_ADDR  = 1                # Modbus ID your reader is configured to listen on
BAUDRATE    = 9600
BYTESIZE    = 8
PARITY      = serial.PARITY_NONE
STOPBITS    = 1
TIMEOUT     = 1.0

# Register mapping (holding registers):
#   0 → voltage (×0.1 V)
#   1 → frequency (×0.1 Hz)
#   2 → current (×0.1 A)
#   3 → active power (×0.1 kW)

instrument = minimalmodbus.Instrument(PORT, SLAVE_ADDR, mode=minimalmodbus.MODE_RTU)
instrument.serial.baudrate = BAUDRATE
instrument.serial.bytesize = BYTESIZE
instrument.serial.parity   = PARITY
instrument.serial.stopbits = STOPBITS
instrument.serial.timeout  = TIMEOUT


def read_and_display(regs):
    #Read the given register addresses and print human-friendly values.
    vals = []
    for addr in regs:
        try:
            v = instrument.read_register(addr, 1)  # one decimal place
            vals.append(v)
        except Exception as e:
            print(f" Error reading R{addr}: {e}")
            return

    print(f"\n--- POLLED VALUES ---")
    print(f" Voltage      : {vals[0]:.1f} V")
    print(f" Frequency    : {vals[1]:.1f} Hz")
    print(f" Current      : {vals[2]:.1f} A")
    print(f" Active Power : {vals[3]:.1f} kW\n")


def fixed_mode():
    print("\nReading registers 0–3:")
    read_and_display([0, 1, 2, 3])


def random_mode():
    regs = random.sample([0, 1, 2, 3], k=4)
    print(f"\n Reading registers in random order: {regs}")
    read_and_display(regs)


def abnormal_mode():
    regs = [10, 11, 12, 13]
    print(f"\nReading invalid registers {regs}:")
    read_and_display(regs)


def main_menu():
    while True:
        print("\nRS-485 Energy Meter Tester")
        print("1. Fixed order Mode")
        print("2. Random order Mode")
        print("3. invalid address Mode")
        print("4. Exit")

        choice = input("Choose mode: ").strip()
        if choice == '1':
            fixed_mode()
        elif choice == '2':
            random_mode()
        elif choice == '3':
            abnormal_mode()
        elif choice == '4':
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid selection, try again.")


if __name__ == "__main__":
    main_menu()
