from pymodbus.client import ModbusSerialClient
import struct
import time

# Configuração do cliente Modbus RTU
client = ModbusSerialClient(
    port='COM4',
    baudrate=9600,
    parity='E',
    stopbits=1,
    bytesize=8,
    timeout=1
)

slave_id = 1  # ID do dispositivo escravo

# Endereços Modbus das saídas analógicas (conforme o manual)
ANALOG_OUTPUT_ADDRESSES = [0x0000, 0x0002, 0x0004, 0x0006]  # 32 bits para cada saída
OUTPUT_MODE_ADDRESS = 0x0514  # Define se é 0-20mA (0x0000) ou 4-20mA (0x0001)

# **Passo 1: Configurar Modo das Saídas (4-20mA)**
mode = 0x0001  # Define 4-20mA
response_mode = client.write_register(OUTPUT_MODE_ADDRESS, mode, slave=slave_id)
if response_mode.isError():
    print("❌ Erro ao configurar modo de operação:", response_mode)
else:
    print("✅ Modo de operação configurado para 4-20mA!")


# **Função para obter valores do usuário com proteção de intervalo**
def get_safe_value(output_number):
    while True:
        try:
            value = float(input(f"Digite o valor para a saída {output_number} (4-20mA): "))
            if 4.0 <= value <= 20.0:
                return value
            else:
                print("⚠️ Valor fora do intervalo permitido! Digite um valor entre 4 e 20 mA.")
        except ValueError:
            print("❌ Entrada inválida! Digite um número válido.")


# **Passo 2: Solicitar valores do usuário**
values_to_write = [get_safe_value(i + 1) for i in range(4)]

# **Passo 3: Escrever valores nas saídas analógicas**
for address, value in zip(ANALOG_OUTPUT_ADDRESSES, values_to_write):
    print(f" escrever {value} mA na saída {address}")


    float_bytes = struct.pack(">f", value)  # Converter float para 4 bytes
    print(f" escrever {float_bytes} ")
    float_words = struct.unpack(">HH", float_bytes)  # Quebrar em 2 registradores de 16 bits

    response = client.write_registers(address, float_words, slave=slave_id)

    if response.isError():
        print(f"❌ Erro ao escrever {value} mA na saída {address}: {response}")
    else:
        print(f"✅ Valor {value} mA escrito com sucesso na saída {address}!")

time.sleep(2)  # Aguarda para garantir que a alteração foi aplicada corretamente

# Fecha a conexão Modbus
client.close()
print("🔌 Conexão encerrada.")