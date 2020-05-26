from Matrix import *
import copy

# a = Matrix("images/lena640x480.pgm")
# a.rotate()
# a.write_to_file('images/new.pgm')
b = Matrix("images/amarelao.ppm")
c = copy.deepcopy(b)
c.noise()
b.invert()
b.rotate()ew.ppm')
