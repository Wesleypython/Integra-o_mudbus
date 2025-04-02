from pymodbus.client.serial import ModbusSerialClient

client = ModbusSerialClient(port='COM4', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=111)

import minimalmodbus
import serial
import time

# Configuração da porta serial
instrument = minimalmodbus.Instrument('COM4', 1)  # Porta serial e ID do escravo
instrument.serial.baudrate = 9600
instrument.serial.timeout = 111  # Timeout de 1 segundo


# Função para escrever valor na saída analógica
def write_analog_output(output_value, mode, initial_value=None):
    try:
        # Escrever valor da saída analógica (endereço 0x0000)
        print(f"Escrevendo valor {output_value} mA na saída analógica...")
        instrument.write_float(0x0100, output_value)  # Escreve como float de 32 bits

        # Escrever modo de operação da saída (endereço 0x0514)
        print(f"Configurando modo de operação da saída para {mode}...")
        instrument.write_register(0x0514, mode, functioncode=0x06)  # Modo 0: 0-20mA, 1: 4-20mA

        # Opcional: Escrever valor inicial de saída (se fornecido)
        if initial_value is not None:
            print(f"Configurando valor inicial da saída para {initial_value} mA...")
            instrument.write_float(0x00C8, initial_value)  # Escreve como float de 32 bits

        print("🎯 Operação de escrita concluída com sucesso!")

    except Exception as e:
        print(f"❌ Erro na escrita: {e}")


# Função para ler as saídas analógicas
def read_analog_outputs():
    try:
        # Lendo valor das saídas analógicas (endereço 0x0000)
        print("Lendo valores das saídas analógicas...")
        analog_value_1 = instrument.read_float(0x0100, functioncode=0x03)  # Lê como float de 32 bits
        analog_value_2 = instrument.read_float(0x0101, functioncode=0x03)  # Para o segundo registro
        analog_value_3 = instrument.read_float(0x0102, functioncode=0x03)
        analog_value_4 = instrument.read_float(0x0103, functioncode=0x03)

        print(f"🔹 Saída Analógica 1: {analog_value_1} mA")
        print(f"🔹 Saída Analógica 2: {analog_value_2} mA")
        print(f"🔹 Saída Analógica 3: {analog_value_3} mA")
        print(f"🔹 Saída Analógica 4: {analog_value_4} mA")

    except Exception as e:
        print(f"❌ Erro na leitura: {e}")


# Exemplo de escrita e leitura das saídas analógicas
def main():
    # Exemplo de escrita
    write_analog_output(10.0, mode=0x0001, initial_value=5.0)  # Escreve 10.0mA, modo 0-20mA, valor inicial 5.0mA

    # Aguardar um pouco antes de ler os valores
    time.sleep(1)

    # Lendo os valores das saídas analógicas
    read_analog_outputs()


# Executando o script principal
if __name__ == "__main__":
    main()

client.close()
