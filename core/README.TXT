===============================
Controle de Saídas Modbus TCP
===============================

Descrição
---------
Este script em Python permite a comunicação com um CLP via protocolo Modbus TCP para controle de saídas analógicas.
Ele foi desenvolvido para configurar e ativar saídas analógicas de módulos EBYTE, com foco em controle de temperatura por meio de
valores enviados para registradores %MW do CLP.


Requisitos

- Python 3.x
- Biblioteca `pymodbus` instalada
- Acesso a um CLP via Modbus TCP (testado com IP: 192.168.3.100, porta 502)


Instalação das dependências:
    pip install pymodbus




Estrutura do Código:
-------------------
1. **Conexão com CLP da Schnneider:**
   - IP e porta configurados para acesso ao CLP via Modbus TCP.


2. **Funções principais:**
   - `config_impar()` – Garante que o valor enviado ative o bit X0 (através de números ímpares).
   - `config_address()` – Permite selecionar qual endereço (registrador) será ativado no CLP.
   - `incrementar()` e `decrementar()` – Seleciona a saída analógica (AO1-AO4) e define o valor de temperatura (4000–20000).
   - `write_memories()` – Envia comandos e valores aos registradores definidos.
   - `write()` – Lógica principal que chama as outras funções e permite execução contínua.






Parâmetros e Registradores

- **Valores aceitos**: Apenas números ímpares (exceto 0 ou 4000 como reset).
- **Temperatura (valor analógico)**: Entre 4000 e 20000 (interpretação depende da lógica do CLP).
- **Endereços permitidos**:
    - De controle digital: 0 a 16 (ex: %MW0)
    - De saída analógica (exemplo para AO1):
        - Controle: %MW600....
        - Valor analógico: %MW610... Conforme valores que programei no ladder

- **Saídas suportadas**: AO1, AO2, AO3, AO4



/////////////************//////////////
Fluxo de Execução

1. Informa-se um endereço de ativação (registrador).
2. Informa-se um valor ímpar para ativação do bit.
3. Informa-se o módulo EBYTE e a saída analógica desejada.
4. O sistema escreve os valores nos registradores definidos.
5. O usuário pode repetir a operação ou encerrar.

Exemplo de Uso



Ao rodar o script:
- Você será solicitado a informar o endereço do registrador (0-16).
- Depois, um valor ímpar (ou 0 para reset).
- Escolher qual saída analógica deseja configurar e a temperatura desejada.
- Os valores são enviados automaticamente ao CLP.




Aviso

Este código foi testado com o CLP Schnneider que interpreta sinais via %MW e módulos EBYTE. Certifique-se de que o endereço,
 mapeamento de registradores e valores estejam de acordo com seu hardware e ladder lógico.

Autor
-----
Desenvolvido por: Wesley  
Trabalho com automação industrial, CLP, Python e controle de módulos analógicos.

