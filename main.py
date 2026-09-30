"""
Sprint 4 - Arquitetura de Computadores
Solução Final: GoodWe Smart Charging Station
"""
from machine import Pin
import time

ev1_g = Pin(2, Pin.OUT)
ev1_y = Pin(3, Pin.OUT)
ev1_r = Pin(4, Pin.OUT)

ev2_g = Pin(6, Pin.OUT)
ev2_y = Pin(7, Pin.OUT)
ev2_r = Pin(8, Pin.OUT)

ev3_g = Pin(10, Pin.OUT)
ev3_y = Pin(11, Pin.OUT)
ev3_r = Pin(12, Pin.OUT)

def set_led_ev(carro_id, status):
    leds = {
        "EV1": (ev1_g, ev1_y, ev1_r),
        "EV2": (ev2_g, ev2_y, ev2_r),
        "EV3": (ev3_g, ev3_y, ev3_r)
    }
    
    p_verde, p_amarelo, p_vermelho = leds[carro_id]
    
    p_verde.value(0)
    p_amarelo.value(0)
    p_vermelho.value(0)
    
    if status == "VERDE": p_verde.value(1)
    elif status == "AMARELO": p_amarelo.value(1)
    elif status == "VERMELHO": p_vermelho.value(1)

def apagar_todos_leds():
    for carro in ["EV1", "EV2", "EV3"]:
        set_led_ev(carro, "OFF")

def mostrar_representacao_dados(valor):
    print("\n[MEMÓRIA] Energia Disponível (Representações):")
    print(f" Decimal:      {valor} W")
    print(f" Hexadecimal:  {hex(valor)}")
    print(f" Binário:      {bin(valor)}")

def gerenciar_energia(energia_disponivel, veiculos):
    energia_restante = energia_disponivel
    demanda_total = sum([v["solicitado"] for v in veiculos])
    
    print(f"\nENERGIA DISPONÍVEL: {energia_disponivel} W")
    for v in veiculos:
        print(f"{v['id']} -> solicita {v['solicitado']} W | Bateria: {v['bateria']:.1f}% (Capacidade: {v['capacidade_kwh']} kWh)")
    print(f"DEMANDA TOTAL:      {demanda_total} W\n")
    
    print("[PROCESSAMENTO] Calculando distribuição e recarga matemática...")
    
    for v in veiculos:
        if energia_restante >= v["solicitado"]:
            v["alocado"] = v["solicitado"]
            v["status"] = "VERDE"
            energia_restante -= v["solicitado"]
            
        elif energia_restante > 0:
            v["alocado"] = energia_restante
            v["status"] = "AMARELO"
            energia_restante = 0 
            
        else:
            v["alocado"] = 0
            v["status"] = "VERMELHO"
            
        # 2. CÁLCULO FÍSICO DE RECARGA (Utilização da ULA do Processador)
        # Transforma W em kW (ex: 2000W = 2kW)
        energia_kwh_entregue = v["alocado"] / 1000  
        
        if energia_kwh_entregue > 0:
            incremento_pct = (energia_kwh_entregue / v["capacidade_kwh"]) * 100
            v["bateria"] += incremento_pct
            
            if v["bateria"] > 100.0:
                v["bateria"] = 100.0
                v["solicitado"] = 0
                v["status"] = "VERDE"
                v["alocado"] = 0
                
    return veiculos

def simular_situacao(numero, titulo, energia_gerada, veiculos):
    print(f"\n{'=' * 75}")
    print(f" SITUAÇÃO {numero} - {titulo}")
    print(f"{'=' * 75}")
    
    mostrar_representacao_dados(energia_gerada)
    veiculos_atualizados = gerenciar_energia(energia_gerada, veiculos)
    
    print(f"\n{'VEÍCULO':<8} | {'BATERIA':<8} | {'SOLICITADO':<10} | {'ALOCADO':<10} | {'LED/STATUS'}")
    print("-" * 75)
    
    for v in veiculos_atualizados:
        if v['status'] == "VERDE": status_txt = "RECARGA ATIVA"
        elif v['status'] == "AMARELO": status_txt = "RECARGA REDUZIDA"
        else: status_txt = "AGUARDANDO/BLOQUEADA"
        
        bateria_formatada = f"{v['bateria']:.1f}%"
        print(f"{v['id']:<8} | {bateria_formatada:<8} | {v['solicitado']:<8} W | {v['alocado']:<8} W | {v['status']} ({status_txt})")
        
        set_led_ev(v['id'], v['status'])
        
    print("-" * 75)
    time.sleep(7)

def main():
    apagar_todos_leds()
    print("Iniciando GoodWe Smart Energy Controller...")
    time.sleep(2)
    
    carros = [
        {"id": "EV1", "bateria": 45.0, "capacidade_kwh": 50, "solicitado": 2000, "alocado": 0, "status": ""},
        {"id": "EV2", "bateria": 20.0, "capacidade_kwh": 75, "solicitado": 2500, "alocado": 0, "status": ""},
        {"id": "EV3", "bateria": 80.0, "capacidade_kwh": 40, "solicitado": 3000, "alocado": 0, "status": ""}
    ]
    
    ciclo = 1
    
    while True:
        print(f"\n\n>>>>>>>> INICIANDO CICLO DE RECARGA {ciclo} <<<<<<<<")
        
        simular_situacao(1, "Alta disponibilidade de energia (8.000 W)", 8000, carros)
        apagar_todos_leds()
        
        simular_situacao(2, "Disponibilidade limitada (5.000 W)", 5000, carros)
        apagar_todos_leds()
        
        simular_situacao(3, "Baixa disponibilidade de energia (2.000 W)", 2000, carros)
        apagar_todos_leds()
        
        print(f"\nFim do ciclo {ciclo}. Salvando dados na memória e aguardando...\n")
        ciclo += 1
        time.sleep(3)

if __name__ == "__main__":
    main()
