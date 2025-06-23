import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

def read_modbus_values(slave_id, client):
    """
    Read seven 32-bit floats from one meter.
    Returns a dict of values.
    """
    def read_reg(addr):
        rr = client.read_holding_registers(address=addr, count=2, unit=slave_id)
        if rr.isError():
            print(f"⚠️  Slave {slave_id} @ {addr}: {rr}")
            return 0.0
        regs = rr.registers
        print(f"  → RAW regs @ {addr}: {regs}")
        decoder = BinaryPayloadDecoder.fromRegisters(
            regs,
            byteorder=Endian.Big,     # bytes are big-endian
            wordorder=Endian.Little   # words are swapped
        )
        return round(decoder.decode_32bit_float(), 3)

    # the seven register offsets you need
    addresses = {
        "V_LL":       132,
        "Voltage":    140,
        "Current":    148,
        "Frequency":  156,
        "Power":      100,
        "PF":         116,
        "Energy":     158,
    }

    return { name: read_reg(addr) for name, addr in addresses.items() }

if __name__ == "__main__":
    client = ModbusClient(
        method='rtu',
        port="/dev/ttyUSB0",
        baudrate=9600,
        parity='E',
        stopbits=1,
        bytesize=8,
        timeout=1
    )

    if not client.connect():
        print("❌ Failed to open serial port. Check USB and permissions.")
        exit(1)

    meter_ids = [1]
    for mid in meter_ids:
        print(f"\nReading Meter #{mid}")
        data = read_modbus_values(mid, client)
        for name, val in data.items():
            print(f"  {name:10s}: {val}")
        time.sleep(0.2)   # small pause

    client.close()
    print("\nAll done.")
