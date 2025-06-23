# RS-485 Energy Meter Simulator & Reader

This project provides two Python scripts for testing RS-485 Modbus RTU communication, typically on a Raspberry Pi using a USB-RS485 adapter:

- **custom_input_slave.py**: Simulates an energy meter as a Modbus RTU slave. You can customize register addresses, values, and data format (single or double register per value).
- **meter_reader_rs485.py**: Reads values from a real or simulated Modbus RTU energy meter.

## Requirements

- Python 3.6+
- USB-RS485 adapter (e.g., `/dev/ttyUSB0` on Linux/Raspberry Pi)
- See `requirements.txt` for Python dependencies.

## Installation

1. Clone or copy this repository to your Raspberry Pi or PC.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### 1. Simulate an Energy Meter (Slave)

Run the slave simulator:
```
python3 custom_input_slave.py
```
- Choose the mode:
  - **Count1**: 1 register per value (16-bit integer)
  - **Count2**: 2 registers per value (32-bit float)
- Enter the register numbers for each measurement as prompted.
- The script will start a Modbus RTU slave on `/dev/ttyUSB0` (Slave ID=1, Even parity).

### 2. Read from an Energy Meter (Master)

Run the reader:
```
python3 meter_reader_rs485.py
```
- The script will attempt to read seven 32-bit float values from a meter (real or simulated) at Slave ID 1.
- Output will show the raw register values and decoded measurements.

## Notes

- Make sure your user has permission to access the serial port (`/dev/ttyUSB0`).
- You can use these scripts to test RS-485 wiring, adapters, and Modbus register mapping.