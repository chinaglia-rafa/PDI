from Matrix import *
import copy

# Carregando a imagem amarelao.ppm para decomposição
a = Matrix("images/amarelao.ppm")
a.decompose()

# Declara imagem PPM que será reconstruída
z = Matrix()
# Seta o formato de z como PPM
z.set_format('P3')

# Carrega um PGM para cada canal RGB
r = Matrix("images/amarelaoR.pgm")
g = Matrix("images/amarelaoG.pgm")
b = Matrix("images/amarelaoB.pgm")

# Compõe uma imagem PPM usando as PGM como canais
z.compose_from_pgm(r, g, b)
z.write_to_file("images/recomposed_01.ppm")
# Embaralha os canais para ver o que acontece
z.compose_from_pgm(g, b, r)
z.write_to_file("images/recomposed_02.ppm")
# Embaralha os canais para ver o que acontece
z.compose_from_pgm(b, r, g)
z.write_to_file("images/recomposed_03.ppm")
