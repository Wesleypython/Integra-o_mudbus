Descrição da estrutura dos códigos
Em todos os arquivos é necessario  a importação das bibliotecas de conexão:
from pymodbus.client import ModbusSerialClient

bibliotecas adicionais:


Write.py

Por Que Converter um Float em Dois Registradores de 16 Bits Antes de Escrever?
# código

for address, value in zip(ANALOG_OUTPUT_ADDRESSES, values_to_write):
    float_bytes = struct.pack(">f", value)  # Converter float para 4 bytes
    float_words = struct.unpack(">HH", float_bytes)  # Quebrar em 2 registradores de 16 bits

    response = client.write_registers(address, float_words, slave=slave_id)

#explicação
O processo de conversão (float → bytes → dois registradores) é necessário devido a três fatores
técnicos fundamentais na comunicação Modbus com dispositivos industriais:

1. Natureza do Protocolo Modbus
O Modbus RTU (usado pelo ME31-XAXA0404) não suporta o tipo de dado float diretamente.
Os comandos padrão do Modbus (como write_registers) só trabalham com registradores de 16 bits (inteiros sem sinal).
Para escrever um float (32 bits), é preciso dividi-lo em dois registradores de 16 bits.


2. Formato do Dado no Dispositivo Escravo
Muitos dispositivos industriais (CLPs, inversores, etc.) armazenam valores analógicos (como corrente, temperatura, etc.) em floats de 32 bits, mas os expõem via Modbus como dois registradores consecutivos.

Exemplo:
Um valor como 20.5 mA (float) é armazenado no dispositivo como:
Registrador 40001: 0x41A4 (parte alta do float).
Registrador 40002: 0x0000 (parte baixa do float).


struct.unpack
20.5 → Bytes: `\x41\xA4\x00\x00`   ----> Onde \x41\xA4\x00\x00 é a representação binária de 20.5 em 32 bits






read_input.py
Biblioteca ou método chamado decode que permite a leitura em miliAmperes:


# O DECODE foi utilizado apenas para fazer a interpretação dos valores em miliamperes
#  BinaryPayloadDecoder da pymodbus é exatamente para isso: interpretar os dois registradores consecutivos como um único valor float32
    resp_float = client.read_input_registers(base_float, count=2, slave=unit_id)
    print("-->",resp_float)
    if not resp_float.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp_float.registers,
            byteorder=Endian.BIG,
            wordorder=Endian.BIG
        )
        val_mA = decoder.decode_32bit_float() # Float mA
    else:
        val_mA = "Erro"