from pymodbus.exceptions import ModbusIOException
import threading
import time
from pymodbus.client import ModbusTcpClient, ModbusSerialClient

# Configuração do cliente Modbus TCP
client = ModbusTcpClient(
    host='192.168.3.7',
    port=502,              # Port default of the Modbus TCP
    timeout=1
)
# client = ModbusSerialClient(
#     port='COM3',
#     baudrate=9600,
#     parity='N',
#     stopbits=1,
#     bytesize=8,
#     timeout=1
# )
print(client)
client.connect()


parar_leitura = False
unit_id=1



# Espera o comando para parar a leitura
def escutar_terminal():
    global parar_leitura
    while True:
        comando = input("Digite 'parar' para cancelar a tentativa de conexão: ")
        if comando.strip().lower() == "parar":
            parar_leitura = True
            break



def aguardar_conexao_modbus():
    global parar_leitura
    print(" Tentando conectar com o dispositivo Modbus...")

    while not parar_leitura:
        try:
            resposta = client.read_input_registers(101, count=1, slave=unit_id)
            if not resposta.isError():
                print("✅ Dispositivo Modbus respondeu corretamente!")
                return True  # conexão estabelecida
            else:
                print(" Erro de comunicação Modbus\n")
                time.sleep(3)
        except ModbusIOException as e:
            print(" Erro de comunicação Modbus: \t", e)
            time.sleep(3)


    print("⛔ Conexão cancelada pelo usuário.")
    return False  # conexão não estabelecida
if parar_leitura == False:   # Fiz essa condição de leitura para que o teste de conexão seja executado na primeira chamada
   aguardar_conexao_modbus()


def ler_AI(idx):
    base_int = 100 + idx    #O idx é apenas um índice da função de leitura e quem altera os valores é o for que chama a função
    # base_float = 200 + idx * 2  #Float ocupa 2 registros, no python as operações tem peso hierarco por ordem de escrita
    #Inteiro µA
    try:
        resp_int = client.read_input_registers(base_int, count=1, slave=unit_id)
        if not resp_int.isError():
             val_uA = resp_int.registers[0]
        else:
            val_uA = 0
    except ModbusIOException as erro:
        print(f" Erro de comunicação ao ler AI{idx}: {erro}")
        val_uA = 0

    return val_uA
          # val_mA


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



def printando(leituras,filtro_equal, range_read):

    # Exibindo os valores
    print("📊 RESULTADOS ANALÓGICOS")
    for i, (ua) in enumerate(leituras, start=1):
        print("Canal AI{}: {} µA | {} mA".format(i,ua, ua/1000))

    print(f"Filtro AI: {filtro_equal}")
    print(f"Faixa de corrente: {range_read}")




# tive que importar o modbus exception
def escutar_terminal():
    global parar_leitura
    while True:
        comando = input("Digite 'parar' para encerrar a leitura: ")#Só aparece se digitar algo no terminal.
        if comando.strip().lower() == "parar":
            parar_leitura = True
            break




# Integrar nessa função um try com o excepty e também um loop para validar a se o componente ebyte ainda esta conectado. para PRINTAR
# UM erro.
def loop_read():
    if not aguardar_conexao_modbus():
        client.close()
        return
    while not parar_leitura:
        # Chamando as funções
        leituras = [ler_AI(i) for i in range(4)]  # quantidade de leitura das AIs, sabendo que cada leitura estará
                                                  # em uma tupla diferente ler_AI(i) e depois dentro da lista
        filtro_equal = filtro_function()
        range_read = faixa_de_leitura()
        printando(leituras, filtro_equal, range_read)


        time.sleep(3)  # Intervalo
    client.close()

# Inicia thread para escutar o terminal
thread_input = threading.Thread(target=escutar_terminal)
thread_input.start()

# Inicia o loop principal de leitura
loop_read()
