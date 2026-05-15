import pygame
import sys
import actions  # Importa o arquivo de lógica de luta
from config import *  # Importa todas as configurações do arquivo config.py

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA)) #Criar a janela da simulação
relogio = pygame.time.Clock() #relógio que conta o tempo do projeto

spr_sheet_spartan = pygame.image.load('Sprites/spartan.png').convert_alpha() #carrega a spritesheet do espartano



#Bloco do agente 1
agente1 = {
    'x': 100,
    'y': CHAO_Y,
    'vel_y': 0,
    'vida': VIDA_INICIAL,
    'direcao': 1,
    'estado': 'neutro',
    'nochao': True,
    'frame': 0,
    'timer_frame': 0
}


#bloco do agente 2
agente2 = {
    'x': 600,
    'y': CHAO_Y,
    'vel_y': 0,
    'vida': VIDA_INICIAL,
    'direcao': -1,
    'estado': 'neutro',
    'nochao': True,
    'frame': 0,
    'timer_frame': 0
    
}

acao_IA1 = 0 
acao_IA2 = 0
distancia = abs(agente1['x'] - agente2['x'])


def obter_estado_completo(a1, a2):
    return (a1['x'], a1['y'], a1['vida'], a1['estado'], 
            a2['x'], a2['y'], a2['vida'], a2['estado'])

def obter_estadoa1():
    return (agente1['x'], agente1['y'], agente1['vida'], agente1['estado'])

def obter_estadoa2():
    return (agente2['x'], agente2['y'], agente2['vida'], agente2['estado'])

def desenhar_agente(agente, tela):
    linha = 0
    coluna = 0
    animando = False

    # 1. DEFINIÇÃO DA LINHA BASEADA NO ESTADO
    if agente['estado'] == 'neutro':
        linha = 0
        coluna = 0
    
    elif agente['estado'] == 'aereo':
        linha = 2
        animando = True # O pulo continua animando
        
    elif agente['estado'] == 'atacandoL': # Ataque Leve
        linha = 0
        animando = True
        
    elif agente['estado'] == 'atacandoG': # Ataque Pesado (Ação 9/G)
        linha = 1 # Se na sua sheet o ataque pesado for linha 2, mude para 1
        animando = True

    # 2. LÓGICA DE MOVIMENTO (SPRITES FIXOS)
    # Se estiver no chão e não estiver atacando, checamos se está andando
    if agente['nochao'] and 'atacando' not in agente['estado']:
        keys = pygame.key.get_pressed()
        
        # Agente 1 (Exemplo com setas ou WASD, ajuste conforme seu input)
        movendo_frente = (agente['direcao'] == 1 and keys[pygame.K_RIGHT]) or (agente['direcao'] == -1 and keys[pygame.K_LEFT])
        movendo_tras = (agente['direcao'] == 1 and keys[pygame.K_LEFT]) or (agente['direcao'] == -1 and keys[pygame.K_RIGHT])

        if movendo_frente:
            linha = 0 # Linha 1
            coluna = 2 # Sprite 3 (Índice 2)
            animando = False
        elif movendo_tras:
            linha = 5 # Linha 6 (Índice 5)
            coluna = 0 # Sprite 1 (Índice 0)
            animando = False

    # 3. CONTROLE DE ANIMAÇÃO
    if animando:
        agente['timer_frame'] += 1
        if agente['timer_frame'] >= 18:
            agente['frame'] = (agente['frame'] + 1) % 3
            agente['timer_frame'] = 0
        coluna = agente['frame']
    else:
        agente['timer_frame'] = 0
        # Se não estiver animando e não for movimento, coluna volta a 0 (neutro)
        if not (movendo_frente or movendo_tras):
            coluna = 0

    # 4. RENDERIZAÇÃO
    area_corte = (coluna * 256, linha * 256, 256, 256)
    sprite = spr_sheet_spartan.subsurface(area_corte)
    
    if agente['direcao'] == -1:
        sprite = pygame.transform.flip(sprite, True, False)
    
    # Alinhamento no chão
    pos_y_alinhada = agente['y'] - 184 #esse valor encaixa perfeitamente, NÃO ALTERAR!!!
    pos_x_alinhada = agente['x'] - 128
    tela.blit(sprite, (pos_x_alinhada, pos_y_alinhada))

#Os eventos do jogo
while True:
    # 1. RESET DE INTENÇÕES
    # Todo frame começa sem nenhuma ação pendente
    acao_IA1 = 0
    acao_IA2 = 0
    
    # 2. ENTRADA DE DADOS
    distancia = abs(agente1['x'] - agente2['x'])
    keys = pygame.key.get_pressed()
    
    # DEFESA: Verificamos se a tecla está segurada
    if keys[pygame.K_h]: 
        acao_IA1 = 4
    if keys[pygame.K_m]: 
        acao_IA2 = 4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Agente 1
            if event.key == pygame.K_f: acao_IA1 = 7 # Soco
            if event.key == pygame.K_g: acao_IA1 = 9 # Chute
            if event.key == pygame.K_t: acao_IA1 = 12 # Mudar Direção
            if event.key == pygame.K_SPACE:
                # Chama o processar_acao com a constante PULAR (que é 2)
                agente1, agente2 = actions.processar_acao(agente1, agente2, actions.PULAR)
            
            # Agente 2
            if event.key == pygame.K_DOWN: acao_IA2 = 7 # Soco
            if event.key == pygame.K_k: acao_IA2 = 9 # Chute
            if event.key == pygame.K_r: acao_IA2 = 12 # Mudar Direção
            
    # Comandos de Movimento (Pulo e Andar)
    if keys[pygame.K_w] and agente1['nochao']:
        acao_IA1 = 1 # Intenção: Pular
    if keys[pygame.K_UP] and agente2['nochao']:
        acao_IA2 = 1 # Intenção: Pular

    # --- EXECUÇÃO DAS AÇÕES ---
    
    # Verificamos se alguém está defendendo antes de calcular o dano
    a1_defendendo = (acao_IA1 == 4)
    a2_defendendo = (acao_IA2 == 4)

    # Processar ataques
    agente1, agente2 = actions.processar_acao(agente1, agente2, acao_IA1)
    agente2, agente1 = actions.processar_acao(agente2, agente1, acao_IA2)   

    # 4. MOVIMENTAÇÃO LATERAL (Sempre ativa)
    if keys[pygame.K_a]: agente1['x'] -= VELOCIDADE_MOVIMENTO
    if keys[pygame.K_d]: agente1['x'] += VELOCIDADE_MOVIMENTO
    if keys[pygame.K_LEFT]: agente2['x'] -= VELOCIDADE_MOVIMENTO
    if keys[pygame.K_RIGHT]: agente2['x'] += VELOCIDADE_MOVIMENTO

    #5: a lógica da física
    # 1. Aplica gravidade
    agente1['vel_y'] += GRAVIDADE
    agente2['vel_y'] += GRAVIDADE

    # 2. Move no eixo Y
    agente1['y'] += agente1['vel_y']
    agente2['y'] += agente2['vel_y']

    # 3. Colisão com o Chão Agente 1
    if agente1['y'] >= CHAO_Y:
        agente1['y'] = CHAO_Y
        agente1['vel_y'] = 0
        agente1['nochao'] = True
        # Se ele estava no ar, volta para o estado neutro ao pousar
        if agente1['estado'] == 'aereo':
            agente1['estado'] = 'neutro'

    # 4. Colisão com o Chão Agente 2
    if agente2['y'] >= CHAO_Y:
        agente2['y'] = CHAO_Y
        agente2['vel_y'] = 0
        agente2['nochao'] = True
        if agente2['estado'] == 'aereo':
            agente2['estado'] = 'neutro'
            
    # Impede de sair da tela
    agente1['x'] = max(0, min(agente1['x'], LARGURA - AGENTE_LARGURA))
    agente2['x'] = max(0, min(agente2['x'], LARGURA - AGENTE_LARGURA))

    agente1['vida'] = max(0, agente1['vida']) #garante que a vida do agente 1 não fique negativa
    agente2['vida'] = max(0, agente2['vida']) #garante que a vida do agente 2 não fique negativa
    
    #parte 6: a renderização
    tela.fill((30,30,30)) #cor cinza para o fundo
    pygame.draw.rect(tela, (100, 100, 100), (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y)) #desenha o chão
    
    desenhar_agente(agente1, tela)
    desenhar_agente(agente2, tela)
    
    #Desenho das barras de vida
    largura_barra = LARGURA *0.2 #20% da largura da tela
    altura_barra = ALTURA * 0.05 #5% da altura da tela
    margem_barra = 20 #margem entre a barra e a borda da tela
    
    #cálculo de preenchimento
    percentual_vida_a1 = agente1['vida'] / VIDA_INICIAL
    percentual_vida_a2 = agente2['vida'] / VIDA_INICIAL
    
    #Desenho da barra do agente 1
    pygame.draw.rect(tela, (255,0,0), (margem_barra, margem_barra, largura_barra, altura_barra)) #fundo vermelho
    pygame.draw.rect(tela, (0,255,0), (margem_barra, margem_barra, largura_barra * percentual_vida_a1, altura_barra)) #preenchimento verde
    
    #Desenho da barra do agente 2
    x_barra2 = LARGURA - largura_barra - margem_barra
    pygame.draw.rect(tela, (255,0,0), (x_barra2, margem_barra, largura_barra, altura_barra)) #fundo vermelho
    pygame.draw.rect(tela, (0, 255, 0), (x_barra2 + (largura_barra * (1 - percentual_vida_a2)), margem_barra, largura_barra * percentual_vida_a2, altura_barra)) #preenchimento verde
    
    #atualização de tela e controle de FPS  
    pygame.display.flip() #atualiza a tela
    relogio.tick(60) #define a taxa de atualização para 60 quadros por segundo
  