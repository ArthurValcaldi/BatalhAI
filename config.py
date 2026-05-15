#esse arquivo é o que possui as configurações padrão da simulação
#ao invés de colocar as variáveis dentro do arena.py, elas estão aqui para facilitar a leitura e organização do código
#também ajuda para puxar as informações para outros arquivos
#isso é modularização

# Dimensões da tela
LARGURA = 1800
ALTURA = 800

# Física
GRAVIDADE = 0.4
CHAO_Y = 750 # Centralizar o valor do chão facilita mudar depois

# Atributos dos Agentes
VIDA_INICIAL = 100
VELOCIDADE_MOVIMENTO = 5
FORCA_PULO = -25
AGENTE_LARGURA = 20
AGENTE_ALTURA = 50

# Atributos de Luta (Baseados nas Ações 6-11)
REDUCAO_DEFESA = 0.5  # Toma 50% a menos de dano

DURACAO_PESADO = 50
DURACAO_LEVE = 40

# Ação 6: Ataque Aéreo
DANO_AEREO = 15
ALCANCE_AEREO = 60
DURACAO_AEREO = DURACAO_PESADO

# Ação 7: Ataque Leve Padrão
DANO_LEVE = 10
ALCANCE_LEVE = 80
DURACAO_LEVE = DURACAO_LEVE

# Ação 8: Ataque Leve Alto
DANO_LEVE_ALTO = 12
ALCANCE_LEVE_ALTO = 80
DURACAO_LEVE_ALTO = DURACAO_LEVE

# Ação 9: Ataque Pesado 1 (Longo)
DANO_PESADO_LONGO = 20
ALCANCE_PESADO_LONGO = 140
DURACAO_PESADO_LONGO = DURACAO_PESADO

# Ação 10: Ataque Pesado 2 (Curto)
DANO_PESADO_CURTO = 25
ALCANCE_PESADO_CURTO = 70
DURACAO_PESADO_CURTO = DURACAO_PESADO

# Ação 11: Quebra Guarda
DANO_QUEBRA_GUARDA = 5
ALCANCE_QUEBRA_GUARDA = 60
DURACAO_QUEBRA_GUARDA = DURACAO_LEVE

#Configurações de renderização

SPRITE_SIZE = 256

# Mapeamento exato da nova Spritesheet (Linha = Índice - 1)
LINHA_IDLE_ANDAR = 0   # Col 0: Idle, Col 1: Aguardando, Col 2: Andando
LINHA_DEFESAS = 1      # Col 0: Padrão, Col 1: Baixa, Col 2: Reforçada
LINHA_PULO = 2
LINHA_MERGULHO = 3     # Ataque Aéreo (Ação 6)
LINHA_ATAQUE_L = 4     # Ataque Leve Padrão (Ação 7)
LINHA_ESTADOS = 5      # Col 0: Recuo, Col 1: Stun, Col 2: Derrotado
LINHA_ATAQUE_L_ALTO = 6
LINHA_ATAQUE_P_LONGO = 7
LINHA_ATAQUE_P_CURTO = 8
LINHA_QUEBRA_GUARDA = 9

# Velocidade da animação (quanto menor, mais rápido troca de frame)
frame_delay = 5