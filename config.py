#esse arquivo é o que possui as configurações padrão da simulação
#ao invés de colocar as variáveis dentro do arena.py, elas estão aqui para facilitar a leitura e organização do código
#também ajuda para puxar as informações para outros arquivos
#isso é modularização

# Dimensões da tela
LARGURA = 1800
ALTURA = 800

# Física
GRAVIDADE = 0.5
CHAO_Y = 750 # Centralizar o valor do chão facilita mudar depois

# Atributos dos Agentes
VIDA_INICIAL = 100
VELOCIDADE_MOVIMENTO = 5
FORCA_PULO = -10
AGENTE_LARGURA = 20
AGENTE_ALTURA = 50

# Atributos de Luta (Baseados nas Ações 6-11)
REDUCAO_DEFESA = 0.5  # Toma 50% a menos de dano

DURACAO_PESADO = 40
DURACAO_LEVE = 30

# Ação 6: Ataque Aéreo
DANO_AEREO = 15
ALCANCE_AEREO = 50
DURACAO_AEREO = DURACAO_PESADO

# Ação 7: Ataque Leve Padrão
DANO_LEVE = 10
ALCANCE_LEVE = 60
DURACAO_LEVE = DURACAO_LEVE

# Ação 8: Ataque Leve Alto
DANO_LEVE_ALTO = 12
ALCANCE_LEVE_ALTO = 60
DURACAO_LEVE_ALTO = DURACAO_LEVE

# Ação 9: Ataque Pesado 1 (Longo)
DANO_PESADO_LONGO = 20
ALCANCE_PESADO_LONGO = 120
DURACAO_PESADO_LONGO = DURACAO_PESADO

# Ação 10: Ataque Pesado 2 (Curto)
DANO_PESADO_CURTO = 25
ALCANCE_PESADO_CURTO = 50
DURACAO_PESADO_CURTO = DURACAO_PESADO

# Ação 11: Quebra Guarda
DANO_QUEBRA_GUARDA = 5
ALCANCE_QUEBRA_GUARDA = 40
DURACAO_QUEBRA_GUARDA = DURACAO_LEVE