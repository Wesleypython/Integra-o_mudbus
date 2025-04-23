from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException

client = ModbusSerialClient(
    port='COM4',
    baudrate=9600,
    parity='E',
    stopbits=1,
    bytesize=8,
    timeout=1
)

conectado = client.connect()

if not conectado:
    print("❌ Não foi possível abrir a porta COM.")
else:
    print("✅ Porta COM aberta. Testando comunicação Modbus...")

    unit_id = 1
    try:
        resposta = client.read_input_registers(100, count=1, slave=unit_id)
        if resposta.isError():
            print("❌ Porta COM aberta, mas sem resposta do dispositivo Modbus.")
        else:
            print("✅ Dispositivo Modbus respondeu corretamente!")
    except ModbusIOException as e:
        print("❌ Erro de comunicação Modbus:", e)
