import pygame
import sys
import actions  # Importa o arquivo de lógica de luta
from config import (LARGURA, ALTURA, GRAVIDADE, CHAO_Y, VIDA_INICIAL, VELOCIDADE_MOVIMENTO, FORCA_PULO, DANO_SOCO, ALCANCE_SOCO, AGENTE_LARGURA, AGENTE_ALTURA, DANO_CHUTE, ALCANCE_CHUTE, REDUCAO_DEFESA)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA)) #Criar a janela da simulação
relogio = pygame.time.Clock() #relógio que conta o tempo do projeto

spr_sheet_spartan = pygame.image.load('Sprites/spartan.png').convert_alpha() #carrega a spritesheet do espartano



#Bloco do agente 1
agente1_x = 100
agente1_y = 50
agente1_vel_y = 0
agente1_cor = (0,255,100) #agente 1 é verde
agente1_nochao = True
vida_agente1 = VIDA_INICIAL


#bloco do agente 2
agente2_x = 600
agente2_y = CHAO_Y
agente2_cor = (255,50,0) #agente 2 é vermelho
agente2_vel_y = 0
agente2_nochao = True
vida_agente2 = VIDA_INICIAL

acao_IA1 = 0 #0 = parado, 1 = pular, 2 = socar
acao_IA2 = 0 #0 = parado, 1 = pular, 2 = socar
distancia = abs(agente1_x - agente2_x)


def obter_estado_completo(agente1_y, agente1_x, agente1_nochao, acao_IA1, vida_agente1, agente2_y, agente2_x, agente2_nochao, acao_IA2, vida_agente2, distancia, gravidade,):
    
    return (agente1_y, agente1_x, agente1_nochao, acao_IA1, vida_agente1,
            agente2_y, agente2_x, agente2_nochao, acao_IA2, vida_agente2)

def obter_estadoa1(agente1_y, agente1_x, agente1_nochao, acao_IA1, vida_agente1):
    return (agente1_y, agente1_x, agente1_nochao, acao_IA1, vida_agente1)

def obter_estadoa2(agente2_y, agente2_x, agente2_nochao, acao_IA2, vida_agente2):
    return (agente2_y, agente2_x, agente2_nochao, acao_IA2, vida_agente2)




#Os eventos do jogo
while True:
    # 1. RESET DE INTENÇÕES
    # Todo frame começa sem nenhuma ação pendente
    acao_IA1 = 0
    acao_IA2 = 0
    
    # 2. ENTRADA DE DADOS
    distancia = abs(agente1_x - agente2_x)
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
            if event.key == pygame.K_f: acao_IA1 = 2 # Soco
            if event.key == pygame.K_g: acao_IA1 = 3 # Chute
            
            # Agente 2
            if event.key == pygame.K_DOWN: acao_IA2 = 2 # Soco
            if event.key == pygame.K_k: acao_IA2 = 3 # Chute
            
    # Comandos de Movimento (Pulo e Andar)
    if keys[pygame.K_w] and agente1_nochao:
        acao_IA1 = 1 # Intenção: Pular
    if keys[pygame.K_UP] and agente2_nochao:
        acao_IA2 = 1 # Intenção: Pular

    # --- EXECUÇÃO DAS AÇÕES (Parte 3 atualizada) ---
    
    # Verificamos se alguém está defendendo antes de calcular o dano
    a1_defendendo = (acao_IA1 == 4)
    a2_defendendo = (acao_IA2 == 4)

    # Processar ataques do Agente 1
    if acao_IA1 in [2, 3]: # Se for Soco (2) ou Chute (3)
        dano = actions.calcular_dano(acao_IA1, distancia, a2_defendendo)
        vida_agente2 -= dano
        if dano > 0: print(f"Agente 1 atingiu o Agente 2! Dano: {dano}")
        else: print("Agente 1 atacou e errou")

    # Processar ataques do Agente 2
    if acao_IA2 in [2, 3]:
        dano = actions.calcular_dano(acao_IA2, distancia, a1_defendendo)
        vida_agente1 -= dano
        if dano > 0: print(f"Agente 2 atingiu o Agente 1! Dano: {dano}")
        else: print("Agente 2 atacou e errou")

    # 4. MOVIMENTAÇÃO LATERAL (Sempre ativa)
    if keys[pygame.K_a]: agente1_x -= VELOCIDADE_MOVIMENTO
    if keys[pygame.K_d]: agente1_x += VELOCIDADE_MOVIMENTO
    if keys[pygame.K_LEFT]: agente2_x -= VELOCIDADE_MOVIMENTO
    if keys[pygame.K_RIGHT]: agente2_x += VELOCIDADE_MOVIMENTO

    #5: a lógica da física
    agente1_vel_y += GRAVIDADE
    agente1_y += agente1_vel_y
    if agente1_y >= CHAO_Y:
        agente1_y = CHAO_Y
        agente1_vel_y = 0
        agente1_nochao = True

    # Agente 2
    agente2_vel_y += GRAVIDADE  
    agente2_y += agente2_vel_y
    if agente2_y >= CHAO_Y:
        agente2_y = CHAO_Y
        agente2_vel_y = 0
        agente2_nochao = True
    # Impede de sair da tela
    agente1_x = max(0, min(agente1_x, LARGURA - AGENTE_LARGURA))
    agente2_x = max(0, min(agente2_x, LARGURA - AGENTE_LARGURA))

    vida_agente1 = max(0, vida_agente1) #garante que a vida do agente 1 não fique negativa
    vida_agente2 = max(0, vida_agente2) #garante que a vida do agente 2 não fique negativa
    
    #parte 6: a renderização
    tela.fill((30,30,30)) #cor cinza para o fundo
    pygame.draw.rect(tela, (100, 100, 100), (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y)) #desenha o chão
    
    #Alinha a posição dos agentes no offset dos sprites para que eles fiquem centralizados
    pos_a1y_alinhada = agente1_y - 184
    pos_a1x_alinhada = agente1_x - 88
    pos_a2y_alinhada = agente2_y - 184
    pos_a2x_alinhada = agente2_x - 88
    
    tela.blit(spr_sheet_spartan, (pos_a1x_alinhada,pos_a1y_alinhada), (0, 0, 256, 256)) #desenha o espartano no agente 1
    
    tela.blit(spr_sheet_spartan, (pos_a2x_alinhada,pos_a2y_alinhada), (0, 0, 256, 256)) #desenha o espartano no agente 2

    #Desenho das barras de vida
    largura_barra = LARGURA *0.2 #20% da largura da tela
    altura_barra = ALTURA * 0.05 #5% da altura da tela
    margem_barra = 20 #margem entre a barra e a borda da tela
    
    #cálculo de preenchimento
    percentual_vida_a1 = vida_agente1 / VIDA_INICIAL
    percentual_vida_a2 = vida_agente2 / VIDA_INICIAL
    
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
  