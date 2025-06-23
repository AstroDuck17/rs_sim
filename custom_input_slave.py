#!/usr/bin/env python3
import sys
import logging

from pymodbus.server.sync import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSparseDataBlock
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

# Configure logging to show only errors
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

# Fixed measurement values: [Voltage*10, Frequency*10, Current*10, Power*10]
fixed_values = [2200, 1200, 500, 1150]

# Helper: prompt user for custom register addresses
# This time we use the register number exactly as entered
# (1-based registers will be used directly)
def get_registers():
    print("Enter custom Modbus register numbers for each measurement:")
    regs = {}
    regs['voltage']   = int(input("  Voltage register #: "))
    regs['frequency'] = int(input("  Frequency register #: "))
    regs['current']   = int(input("  Current register #: "))
    regs['power']     = int(input("  Power register #: "))
    return regs

# Create context for count1: 1 register per value
# Use the exact register as entered by the user
def create_context_count1(values, addr_map):
    regs = {}
    for key, raw in zip(['voltage','frequency','current','power'], values):
        addr = addr_map[key]
        regs[addr] = raw  # raw integer goes directly into that register
    slave_ctx = ModbusSlaveContext(hr=ModbusSparseDataBlock(regs))
    return ModbusServerContext(slaves={1: slave_ctx}, single=False)

# Create context for count2: 2 registers per value
# Each 32-bit float spans two consecutive registers: starting at the user-entered address
def create_context_count2(values, addr_map):
    regs = {}
    for key, raw in zip(['voltage','frequency','current','power'], values):
        addr0 = addr_map[key]
        val = raw / 10.0  # convert to float
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_32bit_float(val)
        high, low = builder.to_registers()
        regs[addr0]     = high  # high word in the user-specified register
        regs[addr0 + 1] = low   # low word in the next register
    slave_ctx = ModbusSlaveContext(hr=ModbusSparseDataBlock(regs))
    return ModbusServerContext(slaves={1: slave_ctx}, single=False)

# Run Modbus RTU slave with even parity / Slave ID = 1
def run_modbus_server(context):
    StartSerialServer(
        context,
        framer=ModbusRtuFramer,
        port="/dev/ttyUSB0",
        baudrate=9600,
        parity='E',    # even parity
        stopbits=1,
        bytesize=8,
        method='rtu'
    )

# Display helper
def display_values(label, values, count):
    print(f"\n--- {label} (count={count}) ---")
    print(f"Voltage:   {values[0] / 10.0:.1f}")
    print(f"Frequency: {values[1] / 10.0:.1f}")
    print(f"Current:   {values[2] / 10.0:.1f}")
    print(f"Power:     {values[3] / 10.0:.1f}\n")

# Mode functions
def mode_count1():
    addr_map = get_registers()
    display_values("Count1 Mode", fixed_values, 1)
    run_modbus_server(create_context_count1(fixed_values, addr_map))


def mode_count2():
    addr_map = get_registers()
    display_values("Count2 Mode", fixed_values, 2)
    run_modbus_server(create_context_count2(fixed_values, addr_map))

# Main menu
def main_menu():
    while True:
        print("\nRS-485 Energy Meter Tester (Slave ID=1, Parity=Even)")
        print("1. Count1 Mode: 1 register/value")
        print("2. Count2 Mode: 2 registers/value (32-bit floats)")
        print("3. Exit")
        choice = input("Choose mode: ")
        if choice == '1':
            mode_count1()
        elif choice == '2':
            mode_count2()
        elif choice == '3':
            print("Exiting tester.")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
