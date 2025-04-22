import threading
import time

def tarefa():
    while True:
        print("Executando tarefa em paralelo... \n")
        time.sleep(1)

# Cria uma thread
trede=threading.Thread(target=tarefa)
trede.start()



def tarefa2():
    for i in range(0,100):
        print(i)
        time.sleep(1)
# Inicia a thread

tarefa2()