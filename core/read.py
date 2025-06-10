import struct
import time
from pymodbus.client import ModbusTcpClient

# Configuração do cliente Modbus TCP
client = ModbusTcpClient(
    host='192.168.3.7',
    port=502,
    timeout=1
)

# client = ModbusTcpClient(
#     host='192.168.3.7',
#     port=502,
#     timeout=1
# )

client.connect()
slave_id =2
# slave_id =2




analog_read_address = 0x0000
num_registers = 8


def convert_to_float(reg1, reg2):
    raw = struct.pack('>HH', reg1, reg2)
    return struct.unpack('>f', raw)[0]




def read_valor_input():
    response = client.read_holding_registers(address=analog_read_address, count=num_registers, slave=slave_id)
    if response.isError():
        print(" Erro ao ler as saídas analógicas:", response)
        return None
    registers = response.registers
    analog_value_1 = convert_to_float(registers[0], registers[1])
    analog_value_2 = convert_to_float(registers[2], registers[3])
    analog_value_3 = convert_to_float(registers[4], registers[5])
    analog_value_4 = convert_to_float(registers[6], registers[7])
    return analog_value_1, analog_value_2, analog_value_3, analog_value_4



# Função para exibir os valores
def exibindo(valores):
    print(f"🔹 Saída Analógica 1: {valores[0]:.2f} mA")
    print(f"🔹 Saída Analógica 2: {valores[1]:.2f} mA")
    print(f"🔹 Saída Analógica 3: {valores[2]:.2f} mA")
    print(f"🔹 Saída Analógica 4: {valores[3]:.2f} mA")
    print("-" * 40)





try:
    while True:
        analogico = read_valor_input()
        if analogico:
            exibindo(analogico)# chama a função e passa os parametros do analógico.
        time.sleep(2)  # Aguarda 2 segundos antes da próxima leitura
except KeyboardInterrupt:
    print(" Leitura interrompida pelo usuário.")
finally:
    client.close()
    print("🔌 Conexão encerrada.")
