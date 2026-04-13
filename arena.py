import pygame
import sys
from config import LARGURA, ALTURA, GRAVIDADE, CHAO_Y, VIDA_INICIAL, VELOCIDADE_MOVIMENTO, FORCA_PULO, DANO_SOCO, DISTANCIA_CONTATO, AGENTE_LARGURA, AGENTE_ALTURA

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA)) #Criar a janela da simulação
relogio = pygame.time.Clock() #relógio que conta o tempo do projeto

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




#parte 1: os eventos do jogo
while True:
    # 1. RESET DE INTENÇÕES
    # Todo frame começa sem nenhuma ação pendente
    acao_IA1 = 0
    acao_IA2 = 0
    
    # 2. ENTRADA DE DADOS
    distancia = abs(agente1_x - agente2_x)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Comandos de "Um Clique" (Soco)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                acao_IA1 = 2 # Intenção: Socar
            if event.key == pygame.K_DOWN:
                acao_IA2 = 2 # Intenção: Socar

    # Comandos de Movimento (Pulo e Andar)
    if keys[pygame.K_w] and agente1_nochao:
        acao_IA1 = 1 # Intenção: Pular
    if keys[pygame.K_UP] and agente2_nochao:
        acao_IA2 = 1 # Intenção: Pular

    # --- ESPAÇO PARA A IA ---
    # No futuro, o código do Luiz Paulo vai apenas dizer:
    # acao_IA1 = cérebro.decidir() 
    # E o resto do código abaixo vai funcionar sozinho!
    # ------------------------

    # 3. EXECUÇÃO DAS AÇÕES
    # Execução Agente 1
    if acao_IA1 == 1: # Pular
        agente1_vel_y = FORCA_PULO
        agente1_nochao = False
    elif acao_IA1 == 2: # Socar
        if distancia < DISTANCIA_CONTATO:
            vida_agente2 -= DANO_SOCO
            print("Ação Executada: Agente 1 socou e acertou!")
        else:
            print("Ação Executada: Agente 1 socou, mas errou!")

    # Execução Agente 2
    if acao_IA2 == 1: # Pular
        agente2_vel_y = FORCA_PULO
        agente2_nochao = False
    elif acao_IA2 == 2: # Socar
        if distancia < DISTANCIA_CONTATO:
            vida_agente1 -= DANO_SOCO
            print("Ação Executada: Agente 2 socou e acertou!")
        else:
            print("Ação Executada: Agente 2 socou, mas errou!")

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
    pygame.draw.rect(tela, agente1_cor, (agente1_x, agente1_y, AGENTE_LARGURA, AGENTE_ALTURA)) #desenha o "boneco em cor RGB verde e com as dimensões 20x50
    pygame.draw.rect(tela, agente2_cor, (agente2_x, agente2_y, AGENTE_LARGURA, AGENTE_ALTURA)) #desenha o agente 2
    pygame.draw.rect(tela, (255, 0, 0), (20, 20, 200, 20)) #parte vermelha (fundo da barra de vida)
    pygame.draw.rect(tela, (0, 255, 0), (20, 20, vida_agente1 * 2, 20)) #parte verde (vida real do agente 1)
    
    pygame.draw.rect(tela, (255, 0, 0), (580, 20, 200, 20)) #parte vermelha (fundo da barra de vida)
    pygame.draw.rect(tela, (0, 255, 0), (580, 20, vida_agente2 * 2, 20)) #parte verde (vida real do agente 2)

    pygame.display.flip() #atualiza a tela
    relogio.tick(60) #define a taxa de atualização para 60 quadros por segundo
  