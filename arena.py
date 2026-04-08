import pygame
import sys

pygame.init()

LARGURA = 800
ALTURA = 400
tela = pygame.display.set_mode((LARGURA, ALTURA)) #Criar a janela da simulação
relogio = pygame.time.Clock() #relógio que conta o tempo do projeto

#Variáveis padrão
gravidade = 0.5

#Bloco do agente 1
agente1_x = 100
agente1_y = 50
agente1_vel_y = 0
agente1_cor = (0,255,100) #agente 1 é verde
agente1_nochao = True


#bloco do agente 2
agente2_x = 600
agente2_y = 330
agente2_cor = (255,50,0) #agente 2 é vermelho
agente2_vel_y = 0
agente2_nochao = True 

def obter_estado(agente1_y, agente2_y, agente1_x, agente2_x, agente1_nochao, agente2_nochao):
    return (agente1_y, agente2_y, agente1_x, agente2_x, agente1_nochao, agente2_nochao)

acao_IA1 = 0 #0 = parado, 1 = pular, 2 = socar
acao_IA2 = 0 #0 = parado, 1 = pular, 2 = socar

#parte 1: os eventos do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #verifica se uma tecla foi pressionada
           if event.key == pygame.K_SPACE: #Se a tecla pressionada for a barra de espaço, o boneco pula
            agente1_vel_y = -10 #define a velocidade vertical do agente 1 para um valor negativo, fazendo com que ele suba
        if acao_IA1 == 1 and agente1_nochao:
            agente1_vel_y = -10
            agente1_nochao = False
        if agente1_y > 330:
            agente1_y = 330
            agente1_vel_y = 0
            agente1_nochao = True
            

    estado_atual = obter_estado(agente1_y, agente2_y, agente1_x, agente2_x, agente1_nochao, agente2_nochao) #obtém o estado atual do jogo 
    print(estado_atual) #imprime o estado atual para debug 

    #parte 2: a lógica da física
    agente1_vel_y += gravidade
    agente1_y += agente1_vel_y
    if agente1_y >= 330:
        agente1_y = 330
        agente1_vel_y = 0
        agente1_nochao = True

    # Agente 2
    agente2_vel_y += gravidade
    agente2_y += agente2_vel_y
    if agente2_y >= 330:
        agente2_y = 330
        agente2_vel_y = 0
        agente2_nochao = True

    #parte 3: a renderização
    tela.fill((30,30,30)) #cor cinza para o fundo
    pygame.draw.rect(tela, agente1_cor, (agente1_x, agente1_y, 20, 50)) #desenha o "boneco em cor RGB verde e com as dimensões 20x50
    pygame.draw.rect(tela, agente2_cor, (agente2_x, agente2_y, 20, 50)) #desenha o agente 2

    pygame.display.flip() #atualiza a tela
    relogio.tick(60) #define a taxa de atualização para 60 quadros por segundo (o VScode completando os comentários para mim é muito bom véi kakaka)
  