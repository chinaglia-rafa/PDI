from Matrix import *
import copy

# Carregando a imagem lena640x480.pgm para testar arquivos PGM
a = Matrix("images/lena640x480.pgm")
# Testa a rotação
for i in range(4):
    a.rotate()
# Escurece a imagem
a.darken(50)
# Clareia a imagem para voltar ao estado anterior
a.lighten(50)
# Leva os valores dos pixels para os extremos de acordo com a metade do limite
a.black_and_white()
# Escreve um arquivo pgm
a.write_to_file('images/new.pgm')
# Carrega um arquivo PPM
b = Matrix("images/amarelao.ppm")
# Copia o objeto para ser destruído usando o método noise()
c = copy.deepcopy(b)
# Destroi todos os pixels, substituindo todos os valores dos canais por valores aleatórios
c.noise()
# Inverte as cores
b.invert()
# Adiciona um Noise Filter à imagem PPM
b.add(c)
# Rotaciona 90° em sentido horário
b.rotate()
# Escreve um arquivo PPM
b.write_to_file('images/new.ppm')
