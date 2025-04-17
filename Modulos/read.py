import struct
from pymodbus.client import ModbusSerialClient

# Configuração do cliente Modbus RTU
client = ModbusSerialClient(
    port='COM4',
    baudrate=9600,
    parity='E',
    stopbits=1,
    bytesize=8,
    timeout=111
)


# Endereço inicial para leitura das saídas analógicas
analog_read_address = 0000
num_registers = 8  # 4 saídas analógicas x 2 registradores cada (float 32 bits)
slave_id = 1



# Realizar a leitura dos 8 registros (4 floats)
response = client.read_holding_registers(address=analog_read_address, count=num_registers, slave=slave_id)
print(f" escrever {response} ")
# Verificar se houve erro na leitura
if response.isError():
    print("❌ Erro ao ler as saídas analógicas:", response)
else:
    # Converte os registros lidos para floats de 32 bits
    registers = response.registers


    def convert_to_float(reg1, reg2):
        """Converte dois registros Modbus (16 bits cada) em um float de 32 bits"""
        raw = struct.pack('>HH', reg1, reg2)  # Big-endian
        print(f" escrever {raw}")
        return struct.unpack('>f', raw)[0]  # Converte para float


    # Lendo os valores das saídas analógicas
    analog_value_1 = convert_to_float(registers[0], registers[1])
    analog_value_2 = convert_to_float(registers[2], registers[3])
    analog_value_3 = convert_to_float(registers[4], registers[5])
    analog_value_4 = convert_to_float(registers[6], registers[7])

    # Exibir os valores corrigidos
    print(f"🔹 Saída Analógica 1: {analog_value_1:.2f} mA")
    print(f"🔹 Saída Analógica 2: {analog_value_2:.2f} mA")
    print(f"🔹 Saída Analógica 3: {analog_value_3:.2f} mA")
    print(f"🔹 Saída Analógica 4: {analog_value_4:.2f} mA")

# Fecha a conexão Modbus
client.close()
print("🔌 Conexão encerrada.")
