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
vida_agente1 = 100


#bloco do agente 2
agente2_x = 600
agente2_y = 330
agente2_cor = (255,50,0) #agente 2 é vermelho
agente2_vel_y = 0
agente2_nochao = True
vida_agente2 = 100

def obter_estado(agente1_y, agente2_y, agente1_x, agente2_x, agente1_nochao, agente2_nochao):
    return (agente1_y, agente2_y, agente1_x, agente2_x, agente1_nochao, agente2_nochao)

acao_IA1 = 0 #0 = parado, 1 = pular, 2 = socar
acao_IA2 = 0 #0 = parado, 1 = pular, 2 = socar

#parte 1: os eventos do jogo
while True:
    # Resetamos as ações a cada frame para que o comando não fique "travado"
    acao_IA1 = 0
    acao_IA2 = 0
    keys = pygame.key.get_pressed() #verifica quais teclas estão sendo pressionadas
    distancia = abs(agente1_x - agente2_x) #calcula a distância horizontal entre os dois agentes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

        #Bloco agente 1
        #Movimentação do agente 1

        if acao_IA1 == 1:
            agente1_vel_y = -10 #define a velocidade vertical do agente 1 para um valor negativo, fazendo com que ele suba
        if agente1_y < 330:
            agente1_nochao = False #se o agente 1 estiver no ar, a variável "no chão" é falsa
        if keys[pygame.K_a]:
            agente1_x -= 5 #move pra esquerda
        if keys[pygame.K_d]:
            agente1_x += 5 #move pra direita

        if keys[pygame.K_w] and agente1_nochao:
            acao_IA1 = 1 #ação de pular
            agente1_vel_y = -10 #define a velocidade vertical do agente 1 para um valor negativo, fazendo com que ele suba
            agente1_nochao = False #define que o agente 1 não está mais no chão, para evitar que ele possa pular novamente enquanto estiver no ar
            
        if keys[pygame.K_f]:
            acao_IA1 = 2 #ação de socar
            if distancia < 50:
                vida_agente2 -= 1 #diminui a vida do agente 2 em 1 ponto se o agente 1 socar e acertar
            
        #Bloco do agente 2
        #Movimentação do agente 2
        if keys[pygame.K_LEFT]: 
            agente2_x -= 5
        if keys[pygame.K_RIGHT]: 
            agente2_x += 5
        if keys[pygame.K_UP] and agente2_nochao:
            acao_IA2 = 1
            agente2_vel_y = -10
            agente2_nochao = False
        if keys[pygame.K_DOWN]:
            acao_IA2 = 2
        if distancia < 50:
            vida_agente1 -= 1

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
    # Impede de sair da tela
    agente1_x = max(0, min(agente1_x, LARGURA - 20))
    agente2_x = max(0, min(agente2_x, LARGURA - 20))

    #parte 3: a renderização
    tela.fill((30,30,30)) #cor cinza para o fundo
    pygame.draw.rect(tela, agente1_cor, (agente1_x, agente1_y, 20, 50)) #desenha o "boneco em cor RGB verde e com as dimensões 20x50
    pygame.draw.rect(tela, agente2_cor, (agente2_x, agente2_y, 20, 50)) #desenha o agente 2
    pygame.draw.rect(tela, (255, 0, 0), (20, 20, 200, 20)) #parte vermelha (fundo da barra de vida)
    pygame.draw.rect(tela, (0, 255, 0), (20, 20, vida_agente1 * 2, 20)) #parte verde (vida real do agente 1)
    
    pygame.draw.rect(tela, (255, 0, 0), (580, 20, 200, 20)) #parte vermelha (fundo da barra de vida)
    pygame.draw.rect(tela, (0, 255, 0), (580, 20, vida_agente2 * 2, 20)) #parte verde (vida real do agente 2)

    pygame.display.flip() #atualiza a tela
    relogio.tick(60) #define a taxa de atualização para 60 quadros por segundo (o VScode completando os comentários para mim é muito bom véi kakaka)
  