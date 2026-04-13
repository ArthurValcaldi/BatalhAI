#esse arquivo é o que possui as configurações padrão da simulação
#ao invés de colocar as variáveis dentro do arena.py, elas estão aqui para facilitar a leitura e organização do código
#também ajuda para puxar as informações para outros arquivos
#isso é modularização

# Dimensões da tela
LARGURA = 800
ALTURA = 400

# Física
GRAVIDADE = 0.5
CHAO_Y = 330 # Centralizar o valor do chão facilita mudar depois

# Atributos dos Agentes
VIDA_INICIAL = 100
VELOCIDADE_MOVIMENTO = 5
FORCA_PULO = -10
DANO_SOCO = 10
DISTANCIA_CONTATO = 50
AGENTE_LARGURA = 20
AGENTE_ALTURA = 50