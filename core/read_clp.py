from pymodbus.client import ModbusTcpClient

# IP do CLP e porta Modbus TCP
client = ModbusTcpClient('192.168.3.100', port=502)
client.connect()


def dispositivo():
    while True:
        try:
            id_dispositivo=int(input("Informe em qual dispositivo deseja fazer a leitura, "
                                     "por meio dos endereços no CLP, 1 ou 2 ? "))

            # if id_dispositivo in [1, 2, 3, 4]:
            if id_dispositivo in [1, 2]:
                print(f"Dispositivo selecionado: {id_dispositivo}")
                return id_dispositivo
            else:
                print("Dispositivo inválido. Digite entre 1 e 4.")
        except ValueError:
            print("Entrada inválida. Digite apenas números.")

def input_or_output():
    while True:
        try:
            in_or_out=int(input("deseja fazer a leitura da entrada ou da saída [Input= 1// Output = 2]? "))
            if in_or_out in [1, 2]:
                print(f"Selecionado: {'Entrada' if in_or_out == 1 else 'Saída'}")
                return in_or_out
            else:
                print("Dispositivo inválido. Digite 1 para entrada ou 2 para saída.")

        except ValueError:
            print("Valor inválido. Digite apenas números.")


# Nessa função foi onde eu fiz a pesquisa de quais endereços serão lidos e,
#  a união do dispositivo com o valor (se seria entrada ou saída)
def selecionar_enderecos(id_, address_in_or_out):
    address_disposivo_one_clp=[]
    base_addresses=[]
    while True:
        try:
            entrada = input("Informe até 4 endereços de leitura (ex: 0,1,2,3): ")
            lista = list(map(int, entrada.split(',')))

            if len(lista) > 4:# Assim eu verifico
                print("Você só pode informar até 4 endereços por vez.")
                continue

            if all(addr in [0, 1, 2, 3] for addr in lista): # verifando se os endereços passados são compativeis
                print(f"Endereços selecionados: {lista}")
                if id_ == 1 and address_in_or_out == 1:
                    address_disposivo_one_clp=[120,130,140,150]

                elif id_ == 1 and address_in_or_out == 2:
                    address_disposivo_one_clp=[30,40,50,60]

                elif id_ == 2 and address_in_or_out == 1:
                    address_disposivo_one_clp = [160, 170, 180, 190]

                elif id_ == 2 and address_in_or_out == 2:
                    address_disposivo_one_clp = [70, 80, 90, 100]
                else:
                    print("Combinação de dispositivo e tipo inválida.")
                    continue

                base_addresses = [address_disposivo_one_clp[i] for i in lista]
                return base_addresses
            else:
                print("Algum endereço está fora do intervalo permitido (1 a 4).")
        except ValueError:
            print("Formato inválido. Use vírgulas para separar os endereços.")


# Chamando as funções
address_in_or_out = input_or_output() # Solicita se será leitura de entrada ou saída
id_ = dispositivo()# Solicita qual dispositivo (1 ou 2)
out_address = selecionar_enderecos(id_, address_in_or_out)# Solicita os endereços conforme o dispositivo e o tipo de leitura
escravo = id_# Define qual o escravo Modbus será usado (nesse caso, mesmo que id_, se for compatível)


# Leitura do registrador
def leitura(out_address, escravo):
    for endereco in out_address:
        result = client.read_holding_registers(endereco, count=1, slave=escravo)

        if result.isError():
            print(f"Erro na leitura do endereço {endereco}: {result}")
        else:
            valor = result.registers[0]
            print(f"Valor de %MW{endereco} é: {valor}")


leitura(out_address, escravo) # Chama a função de leitura
client.close()

