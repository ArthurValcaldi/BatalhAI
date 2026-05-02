from config import *

# Mapeamento das ações
PARADO = 1
PULAR = 2
DEFESA_PADRAO = 3
DEFESA_BAIXA = 4
DEFESA_ESPECIAL = 5
ATAQUE_AEREO = 6
ATAQUE_LEVE_PADRAO = 7
ATAQUE_LEVE_ALTO = 8
ATAQUE_PESADO_1 = 9
ATAQUE_PESADO_2 = 10
QUEBRA_GUARDA = 11
MUDAR_DIRECAO = 12

def processar_acao(agente_atacante, agente_defensor, tipo_acao):
    # 1. Verificação de estados
    if agente_atacante['estado'] == 'derrotado':
        return agente_atacante, agente_defensor
    
    # Sistema de Cooldown/Timer (Duração do ataque)
    if agente_atacante.get('timer_acao', 0) > 0:
    # Ataque aéreo não reduz o timer por tempo, ele vai até o chão
        if agente_atacante['estado'] != 'atacandoAereo':
            agente_atacante['timer_acao'] -= 1
        
        if agente_atacante['timer_acao'] <= 0 and agente_atacante['estado'] != 'atacandoAereo':
            agente_atacante['estado'] = 'neutro'
        return agente_atacante, agente_defensor

    # 2. Execução das ações
    if tipo_acao == MUDAR_DIRECAO:
        if agente_atacante['nochao'] and 'atacando' not in agente_atacante['estado']:
            agente_atacante['direcao'] *= -1
            
    #Pular tem prioridade sobre o movimento, então ele é processado antes
    elif tipo_acao == PULAR:
        if agente_atacante['nochao']:
            agente_atacante['vel_y'] = FORCA_PULO
            agente_atacante['nochao'] = False
            agente_atacante['estado'] = 'aereo'
    
    elif 3 <= tipo_acao <= 5: # Defesas
        agente_atacante['estado'] = 'defendendo'

# --- BLOCO DE ATAQUES (6 a 11) ---
    elif 6 <= tipo_acao <= 11:
        # Se for ataque aéreo (6), mas já estiver no chão, ignora
        if tipo_acao == ATAQUE_AEREO and agente_atacante['nochao']:
            return agente_atacante, agente_defensor 

        distancia = abs(agente_atacante['x'] - agente_defensor['x'])  

        # CONFIGURAÇÃO ESPECÍFICA DO ATAQUE AÉREO
        if tipo_acao == ATAQUE_AEREO:
            agente_atacante['estado'] = 'atacandoAereo'
            agente_atacante['timer_acao'] = 999  # Um valor alto para travar outras ações até cair
            agente_atacante['vel_y'] = 15       # O "mergulho" (ajuste conforme o config)
        
        # ATAQUES PESADOS DE TERRA (9 e 10)
        elif tipo_acao in [9, 10]:
            agente_atacante['estado'] = 'atacandoG'
            agente_atacante['timer_acao'] = DURACAO_PESADO if tipo_acao == 9 else DURACAO_PESADO_CURTO
        
        # ATAQUES LEVES (7, 8 e 11)
        else:
            agente_atacante['estado'] = 'atacandoL'
            agente_atacante['timer_acao'] = DURACAO_LEVE

        # PROCESSA O DANO (Independente de qual ataque foi)
        dano = calcular_logica_dano(tipo_acao, distancia, agente_defensor)
        agente_defensor['vida'] -= dano
        
        # Efeito de desequilíbrio para golpes pesados ou chutes
        if dano > 0 and tipo_acao in [9, 11]:
            agente_defensor['estado'] = 'desequilibrado'
            agente_defensor['timer_acao'] = 15 # Stun no inimigo

    elif tipo_acao == PARADO and agente_atacante['nochao']:
        agente_atacante['estado'] = 'neutro'

    return agente_atacante, agente_defensor

def calcular_logica_dano(tipo_acao, distancia, agente_defensor):
    dano_base = 0
    
    # Mapeamento de alcances e danos
    if tipo_acao == ATAQUE_LEVE_PADRAO and distancia < ALCANCE_LEVE:
        dano_base = DANO_LEVE
    elif tipo_acao == ATAQUE_LEVE_ALTO and distancia < ALCANCE_LEVE_ALTO:
        dano_base = DANO_LEVE_ALTO
    elif tipo_acao == ATAQUE_PESADO_1 and distancia < ALCANCE_PESADO_LONGO:
        dano_base = DANO_PESADO_LONGO
    elif tipo_acao == ATAQUE_PESADO_2 and distancia < ALCANCE_PESADO_CURTO:
        dano_base = DANO_PESADO_CURTO
    elif tipo_acao == QUEBRA_GUARDA and distancia < ALCANCE_QUEBRA_GUARDA:
        dano_base = DANO_QUEBRA_GUARDA
    elif tipo_acao == ATAQUE_AEREO and distancia < ALCANCE_AEREO:
        dano_base = DANO_AEREO

    if dano_base == 0: return 0

    # Lógica de defesa
    if agente_defensor['estado'] == 'defendendo':
        if tipo_acao == QUEBRA_GUARDA:
            return dano_base # Ignora defesa
        return dano_base * REDUCAO_DEFESA
    
    return dano_base