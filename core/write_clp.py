from pymodbus.client import ModbusTcpClient
import time
# IP do CLP e porta Modbus TCP
client = ModbusTcpClient('192.168.3.100', port=502)
client.connect()

# Endereçando e permitindo somente a entrada de valores de número impar, para que o valor do
# registrador %MWx.X0(CLP) sejá sempre 1 ao ativar. Pois o sistema de leitura desses registradores são em binário:
# 3= 11 , 5= 101, 7= 111 ... então o primeiro numero ao mandar um valor ímpar sempre permanecerá ativo no CLP.
# A ideia final é que seja 1 sempre que apertar um botão graficamente
def config_odd(): # configurando apenas números impar
    while True:
        try:
            valor = int(input("Informe um valor ímpar para ativar ou o valor 0 para desativar: "))
            if valor % 2 != 0 or valor == 0 or valor ==4000:
                print("Valor válido. Bit X0 será ativado.")
                return valor
            else:
                print("Por favor, digite um número ímpar ou o valor 0.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


# Fazer a escrita manualmente dos endereços, sendo apenas disponiveis os valores utilizados no CLP.
def config_address():
    while True:
        try:
            address= int(input("informe o endereço a ser acionado [0-16]: "))
            if address in [0, 1, 2,3,4,5,6,7,9,10,11,12,13,14,15,16]:
                # ,600, 610, 620, 630, 640, 650, 660, 670
                print("Endereço válido. Os endereços receberá os valores.")
                return address
        except ValueError:
            print("Endereço inválido. Digite um número dentro do range esperado.")


#  Preciso que o usúario escolha qual saída deseja alterar AI1, AI2, AI3, AI4
def increment(aumentar_ou_diminuir):
    while True:
        try:
            enderecamento = int(input('Informe qual EBYTE deseja alterar [1-4]: '))
            enderecamento_ao = str(input('Informe qual saída analógica quer alterar [AO1, AO2, AO3, AO4]: ')).strip().upper()
            temperatura = int(input('Qual a temperatura desejada [4000-20000]?: '))
            if enderecamento == 1 and 4000 <= temperatura <= 20000:
                if enderecamento_ao == 'AO1':
                    return aumentar_ou_diminuir, 600, 610, temperatura
                elif enderecamento_ao == 'AO2':
                    return aumentar_ou_diminuir, 620, 630,temperatura
                elif enderecamento_ao == 'AO3':
                    return aumentar_ou_diminuir, 640, 650,temperatura
                elif enderecamento_ao == 'AO4':
                    return aumentar_ou_diminuir, 660, 670,temperatura
                else:
                    print("Saída analógica inválida.")
            else:
                print("Endereçamento inválido ou temperatura fora do intervalo.")
        except ValueError:
            print("Valores inválidos. Digite os dados corretamente.")

def decrement(aumentar_ou_diminuir):
    while True:
        try:
            enderecamento = int(input('Informe qual EBYTE deseja alterar [1-4]: '))
            enderecamento_ao = str(input('Informe qual saída analógica quer alterar [AO1, AO2, AO3, AO4]: ')).strip().upper()
            temperatura = int(input('Qual a temperatura desejada [4000-20000]?: '))
            if enderecamento == 1 and 4000 <= temperatura <= 20000:
                if enderecamento_ao == 'AO1':
                    return aumentar_ou_diminuir, 600,610, temperatura
                elif enderecamento_ao == 'AO2':
                    return aumentar_ou_diminuir, 620, 630, temperatura
                elif enderecamento_ao == 'AO3':
                    return aumentar_ou_diminuir, 640, 650, temperatura
                elif enderecamento_ao == 'AO4':
                    return aumentar_ou_diminuir, 660, 670, temperatura
                else:
                    print("Saída analógica inválida.")
            else:
                print("Endereçamento inválido ou temperatura fora do intervalo.")
        except ValueError:
            print("Valores inválidos. Digite os dados corretamente.")

def increment_or_decrement():
    while True:
        try:
            aumentar_ou_diminuir = int(input('Deseja incrementar ou decrementar? [1 = incrementar / 2 = decrementar]: '))
            if aumentar_ou_diminuir == 1:
                return increment(aumentar_ou_diminuir)
            elif aumentar_ou_diminuir == 2:
                return decrement(aumentar_ou_diminuir)
            else:
                print("Digite apenas 1 ou 2.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def write_memories():
    # Recebe os valores das funções acima
    aumenta_ou_diminui, address_on, address_ao, valor_passado = increment_or_decrement()


    # Reset dos acionamento do contato no ladder
    reset_result1 = client.write_register(address=address_on, value=0, slave=0)
    if reset_result1.isError():
        print(f"Erro ao enviar reset (0) para %MW{address_on}: {reset_result1}")
    else:
        print(f"Reset enviado com sucesso para %MW{address_on}")

    result1 = client.write_register(address=address_on, value=aumenta_ou_diminui, slave=0)
    result2 = client.write_register(address=address_ao, value=valor_passado, slave=0)

    # Printando que os dados foram enviados.
    print(f"\n=== DADOS ENVIADOS ===")
    print(f"Bit de controle: {aumenta_ou_diminui} -> Registrador %MW{address_on} (memória do CLP)")
    print(f"Temperatura: {valor_passado} -> Registrador %MW{address_ao} (memória do CLP)")

    if result1.isError():
        print(f"Erro ao escrever o bit de controle em %MW{address_on} ")
    else:
        print(f"Bit de controle escrito com sucesso em %MW{address_on} ")

    if result2.isError():
        print(f"Erro ao escrever a temperatura em %MW{address_ao} ")
    else:
        print(f"Temperatura escrita com sucesso em %MW{address_ao} ")


# Leitura do registrador
def write(out_address, valor, quantidade):
    while True:
        # Reset no contato de memoria do CLP que ativa a leitura.
        reset_result = client.write_register(address=out_address, value=0, slave=0)
        if reset_result.isError():
            print(f"Erro ao enviar reset (0) para %MW{out_address}: {reset_result}")
        else:
            print(f"Reset enviado com sucesso para %MW{out_address}")

        time.sleep(0.2)  # Pequeno delay pode ser útil no CLP



        result = client.write_register(address=out_address, value=valor, slave=0)

        if result.isError():
            print("Erro ao escrever no endereço:", result)
        else:
            print(f"Valor {valor} escrito com sucesso em %MW{out_address}")

        write_memories()

        while True:
            x = input('Deseja continuar a ativação de mais alguma leitura dos sensores? [Sim / Não]: ').strip().upper()
            if x in ['NÃO', 'NAO', 'N']:
                return  # Encerra a função
            elif x in ['SIM', 'S']:
                quantidade = 1
                out_address = config_address()
                valor = config_odd()
                break  # Sai da validação e continua com o próximo loop de escrita
            else:
                print("Resposta inválida. Digite apenas 'Sim' ou 'Não'.")




# Execução principal
quantidade = 1
out_address = config_address()
valor = config_odd()
write(out_address, valor, quantidade)
client.close()

