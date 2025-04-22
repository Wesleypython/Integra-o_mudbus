from narwhals.selectors import string
from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import threading
import time
# PRÓXIMA ETAPA É FAZER O LOOP ENQUANTO O USÁRIO NÃO INFORMA UM PARAMETRO




client = ModbusSerialClient(
    port='COM4',
    baudrate=9600,
    parity='E',
    stopbits=1,
    bytesize=8,
    timeout=1
)
client.connect()

unit_id = 1


def ler_AI(idx):
    base_int = 100 + idx    #O idx é apenas um índice da função de leitura e quem altera os valores é o for que chama a função
    base_float = 200 + idx * 2  #Float ocupa 2 registros, no python as operações tem peso hierarco por ordem de escrita
    # Explicação:
    # idx = 0 (AI0):
    # base_int = 100 → valor inteiro (µA) está no registrador 100
    # base_float = 200 → valor float (mA) está nos registradores 200 e 201
    # Se idx = 1 (AI1):
    # base_int = 101
    # base_float = 202 e 203

    #Inteiro µA
    resp_int = client.read_input_registers(base_int, count=1, slave=unit_id)
    val_uA = resp_int.registers[0] if not resp_int.isError() else "Erro"



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

    return val_uA, val_mA


#O filtro aqui se refere a uma configuração que suavisa a leitura para não ficar alterando os valores toda hora.
def filtro_function():# Leitura do filtro e (apenas AI1 como exemplo)
    filtro_resp = client.read_holding_registers(1200, count=1, slave=unit_id)
    filtro = filtro_resp.registers[0] if not filtro_resp.isError() else "Erro"
    return filtro

# Leitura da faixa (apenas AI1 como exemplo)
def faixa_de_leitura():
    range_resp = client.read_holding_registers(1202, count=1, slave=unit_id)
    range_val = range_resp.registers[0] if not range_resp.isError() else "Erro"
    if range_val == 0:
        faixa = "0-20mA"
    else:
        faixa= "4-20mA"
    return faixa


# Leitura do Triggers e modo
high = client.read_holding_registers(8000, count=1, slave=unit_id)
low = client.read_holding_registers(8050, count=1, slave=unit_id)
# pegando somente os registros
trigger_high = high.registers[0] if not high.isError() else "Erro"
trigger_low = low.registers[0] if not low.isError() else "Erro"


trigger_mode_resp = client.read_holding_registers(8100, count=1, slave=unit_id)
trigger_mode = trigger_mode_resp.registers[0] if not trigger_mode_resp.isError() else "Erro"
print("-",trigger_mode)




def printando(leituras,filtro_equal, range_read):
    # Printando os resultados
    print("📊 RESULTADOS ANALÓGICOS")
    for i, (ua, ma) in enumerate(leituras, start=1):
        print(f"Canal AI{i}: {ua} µA | {ma} mA")

    print(f"Filtro AI: {filtro_equal}")
    print(f"Faixa de corrente: {range_read}")


leituras = [ler_AI(i) for i in range(4)] # quantidade de leitura das AIs, sabendo que cada leitura estará
                                 # em uma tupla diferente ler_AI(i) e depois dentro da lista
filtro_equal= filtro_function()
range_read= faixa_de_leitura()
parar_leitura = False  # variável de controle

def escutar_terminal():
    global parar_leitura
    while True:
        comando = input("Digite '/parar' para encerrar a leitura: ")#Só aparece se digitar algo no terminal.
        if comando.strip().lower() == "/parar":
            parar_leitura = True
            break

def loop_read():
    global parar_leitura
    while not parar_leitura:
        printando(leituras, filtro_equal, range_read)
        time.sleep(10)  # pequeno intervalo entre as leituras

    client.close()
    print("Leitura encerrada.")

# Inicia thread para escutar o terminal
thread_input = threading.Thread(target=escutar_terminal)
thread_input.start()

# Inicia o loop principal de leitura
loop_read()
