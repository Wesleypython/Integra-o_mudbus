from pymodbus.client import ModbusSerialClient  # Modbus RTU
import struct
import time

# Configuração do cliente Modbus RTU
client = ModbusSerialClient(
    port='COM4',
    baudrate=9600,
    parity='E',  # Paridade ('N' = None, 'E' = Even, 'O' = Odd)
    stopbits=1,
    bytesize=8,
    timeout=111  # 111 segundos
)

# Função para converter dois registros em um número de ponto flutuante (IEEE 754)
def convert_to_float(reg1, reg2):
    """Converte dois registros Modbus (16 bits cada) em um float de 32 bits"""
    raw = struct.pack('>HH', reg1, reg2)  # Big-endian
    return struct.unpack('>f', raw)[0]  # Converte para float

# Endereço inicial para leitura das entradas analógicas (AI)
analog_input_address = 0x0064  # Endereço da entrada analógica (em unidades de microamperes ou miliamperes)
num_registers = 8  # Número de registros a serem lidos (4 entradas x 2 registradores cada)
slave_id = 1  # ID do dispositivo Modbus

# Realizar a leitura dos 8 registros (4 entradas analógicas x 2 registros)
response = client.read_holding_registers(address=analog_input_address, count=num_registers, slave=slave_id)

# Verificar se houve erro na leitura
if response.isError():
    print("❌ Erro ao ler as entradas analógicas:", response)
else:
    # Converte os registros lidos para floats de 32 bits
    registers = response.registers

    # Lendo os valores das entradas analógicas
    analog_value_1 = convert_to_float(registers[0], registers[1])
    analog_value_2 = convert_to_float(registers[2], registers[3])
    analog_value_3 = convert_to_float(registers[4], registers[5])
    analog_value_4 = convert_to_float(registers[6], registers[7])

    # Exibir os valores corrigidos
    print(f"🔹 Entrada Analógica 1: {analog_value_1:.2f} mA")
    print(f"🔹 Entrada Analógica 2: {analog_value_2:.2f} mA")
    print(f"🔹 Entrada Analógica 3: {analog_value_3:.2f} mA")
    print(f"🔹 Entrada Analógica 4: {analog_value_4:.2f} mA")

# Fecha a conexão Modbus
client.close()
print("🔌 Conexão encerrada.")
