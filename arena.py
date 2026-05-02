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
    'nochao': True
}


#bloco do agente 2
agente2 = {
    'x': 600,
    'y': CHAO_Y,
    'vel_y': 0,
    'vida': VIDA_INICIAL,
    'direcao': -1,
    'estado': 'neutro',
    'nochao': True
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
    agente1['vel_y'] += GRAVIDADE
    agente1['y'] += agente1['vel_y']
    if agente1['y'] >= CHAO_Y:
        agente1['y'] = CHAO_Y
        agente1['vel_y'] = 0
        agente1['nochao'] = True

        # SE ELE ESTAVA ATACANDO NO AR, AGORA ELE PARA
        if agente1['estado'] == 'atacandoAereo':
            agente1['estado'] = 'neutro'
            agente1['timer_acao'] = 0  # Libera o personagem depois do ataque aéreo
            
    # Agente 2
    agente2['vel_y'] += GRAVIDADE  
    agente2['y'] += agente2['vel_y']
    if agente2['y'] >= CHAO_Y:
        agente2['y'] = CHAO_Y
        agente2['vel_y'] = 0
        agente2['nochao'] = True

        # SE ELE ESTAVA ATACANDO NO AR, AGORA ELE PARA
        if agente2['estado'] == 'atacandoAereo':
            agente2['estado'] = 'neutro'
            agente2['timer_acao'] = 0  # Libera o personagem depois do ataque aéreo
            
    # Impede de sair da tela
    agente1['x'] = max(0, min(agente1['x'], LARGURA - AGENTE_LARGURA))
    agente2['x'] = max(0, min(agente2['x'], LARGURA - AGENTE_LARGURA))

    agente1['vida'] = max(0, agente1['vida']) #garante que a vida do agente 1 não fique negativa
    agente2['vida'] = max(0, agente2['vida']) #garante que a vida do agente 2 não fique negativa
    
    #parte 6: a renderização
    tela.fill((30,30,30)) #cor cinza para o fundo
    pygame.draw.rect(tela, (100, 100, 100), (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y)) #desenha o chão
    
    #Alinha a posição dos agentes no offset dos sprites para que eles fiquem centralizados
    pos_a1y_alinhada = agente1['y'] - 184
    pos_a1x_alinhada = agente1['x'] - 88
    pos_a2y_alinhada = agente2['y'] - 184
    pos_a2x_alinhada = agente2['x'] - 88
    
  # --- DESENHAR AGENTE 1 ---
    sprite_a1 = spr_sheet_spartan.subsurface((0, 0, 256, 256))
    if agente1['direcao'] == -1:
        sprite_a1 = pygame.transform.flip(sprite_a1, True, False)
    tela.blit(sprite_a1, (pos_a1x_alinhada, pos_a1y_alinhada))

# --- DESENHAR AGENTE 2 ---
    sprite_a2 = spr_sheet_spartan.subsurface((0, 0, 256, 256))
    if agente2['direcao'] == -1:
        sprite_a2 = pygame.transform.flip(sprite_a2, True, False)
    tela.blit(sprite_a2, (pos_a2x_alinhada, pos_a2y_alinhada))
    
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
  