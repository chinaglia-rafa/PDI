from Matrix import *


a = Matrix()

a.load_from_file("images/lena640x480.pgm")
# a.load_from_file("images/wide.pgm")
# print(a)
a.lighten(10)
a.rotate()
a.invert()
a.darken(30)
a.invert()
a.rotate()
a.write_to_file('images/new.pgm')
