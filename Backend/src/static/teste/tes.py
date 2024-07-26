from graphviz import Digraph

# Criação do diagrama
dot = Digraph(comment='Diagrama de Caso de Uso - Sistema de Controle de Estacionamento')

# Adição dos atores
dot.node('Jogador', shape='plaintext', label='<<actor>>\nJogador')
dot.node('Sistema', shape='rect')

# Adição dos casos de uso
dot.node('Adicionar Palavra/Frase', shape='ellipse')
dot.node('Sortear Palavra/Frase', shape='ellipse')
dot.node('Exibir Palavra/Frase', shape='ellipse')
dot.node('Advinhar Letra', shape='ellipse')
dot.node('Registrar Letra Errada', shape='ellipse')
dot.node('Atualizar Pontuação', shape='ellipse')
dot.node('Exibir Desenho do Boneco', shape='ellipse')
dot.node('Exibir Pontuação', shape='ellipse')

# Definindo as conexões (relações) entre os atores e os casos de uso
dot.edge('Jogador', 'Adicionar Palavra/Frase')
dot.edge('Jogador', 'Sortear Palavra/Frase')
dot.edge('Jogador', 'Exibir Palavra/Frase')
dot.edge('Jogador', 'Advinhar Letra')
dot.edge('Sistema', 'Registrar Letra Errada')
dot.edge('Sistema', 'Atualizar Pontuação')
dot.edge('Sistema', 'Exibir Desenho do Boneco')
dot.edge('Sistema', 'Exibir Pontuação')

# Salvando o diagrama em um arquivo
dot.render('diagrama_caso_de_uso', format='png')

# Exibição do diagrama
print(dot.source)
