from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

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
    base_int = 100 + idx
    base_float = 200 + idx * 2  # float ocupa 2 registros

    # Inteiro µA
    resp_int = client.read_input_registers(base_int, count=1, slave=unit_id)
    val_uA = resp_int.registers[0] if not resp_int.isError() else "Erro"

    # Float mA
    resp_float = client.read_input_registers(base_float, count=2, slave=unit_id)
    if not resp_float.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp_float.registers,
            byteorder=Endian.BIG,
            wordorder=Endian.BIG
        )
        val_mA = decoder.decode_32bit_float()
    else:
        val_mA = "Erro"

    return val_uA, val_mA

# Leitura das 4 AIs
leituras = [ler_AI(i) for i in range(4)]

# Leitura do filtro e faixa (apenas AI1 como exemplo)
filtro_resp = client.read_holding_registers(1200, count=1, slave=unit_id)
filtro = filtro_resp.registers[0] if not filtro_resp.isError() else "Erro"

range_resp = client.read_holding_registers(1202, count=1, slave=unit_id)
range_val = range_resp.registers[0] if not range_resp.isError() else "Erro"
faixa = "0-20mA" if range_val == 0 else "4-20mA"

# Triggers e modo
high = client.read_holding_registers(8000, count=1, slave=unit_id)
low = client.read_holding_registers(8050, count=1, slave=unit_id)
trigger_high = high.registers[0] if not high.isError() else "Erro"
trigger_low = low.registers[0] if not low.isError() else "Erro"

trigger_mode_resp = client.read_holding_registers(8100, count=1, slave=unit_id)
trigger_mode = trigger_mode_resp.registers[0] if not trigger_mode_resp.isError() else "Erro"
modos = ["Desligado", "Subida", "Descida", "Ambos"]
modo_trigger = modos[trigger_mode] if isinstance(trigger_mode, int) and trigger_mode < len(modos) else "Desconhecido"

# Print de resultados
print("📊 RESULTADOS ANALÓGICOS")
for i, (ua, ma) in enumerate(leituras, start=1):
    print(f"Canal AI{i}: {ua} µA | {ma} mA")
print(f"Filtro AI: {filtro}")
print(f"Faixa de corrente: {faixa}")
print(f"Trigger Alto: {trigger_high} µA")
print(f"Trigger Baixo: {trigger_low} µA")
print(f"Modo de Trigger: {modo_trigger}")

client.close()