from config import ALCANCE_SOCO, DANO_SOCO, DANO_CHUTE, ALCANCE_CHUTE, REDUCAO_DEFESA

def calcular_dano(tipo_acao, distancia, defensor_esta_defendendo):
    dano_base = 0
    
    if tipo_acao == 2: # SOCO
        if distancia < ALCANCE_SOCO:
            dano_base = DANO_SOCO
    
    elif tipo_acao == 3: # CHUTE
        if distancia < ALCANCE_CHUTE:
            dano_base = DANO_CHUTE
            
    if defensor_esta_defendendo:
        dano_base *= REDUCAO_DEFESA
    
    return dano_base