import struct
import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient(host='192.168.1.20', port=502, timeout=111)

if client.connect():
    print("✅ Conectado ao dispositivo Modbus TCP!")
    client.close()
else:
    print(" Falha na conexão Modbus TCP.")
