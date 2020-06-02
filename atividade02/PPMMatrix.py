import random
import copy
import re
from PGMMatrixInterface import PGMMatrixInterface

class PPMMatrix():


    def __init__(self):
        # Quantidade de canais por pixel
        self.channels_in_pixel = 3

    def __str__(self):
        return self.__class__.__name__

    def str(self, matrix):
        if matrix.get_size().rows == matrix.get_size().cols == 0:
            return "Matrix is empty! (0x0)"
        s = "   Matrix is %d rows by %d cols\n" % (matrix.get_size().rows, matrix.get_size().cols)
        s += "   Matrix has %d channels\n\n" % (self.channels_in_pixel)
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                for channel in range(self.channels_in_pixel):
                    s += " " + str(pixel[channel])
                s += "|"
            s += "\n"

        return s

    def init(self, matrix):
        """ Inicializa um vetor de tamanho size x size com zeros """

        new_items = []
        for i in range(matrix.get_size().rows):
            row = []
            for j in range(matrix.get_size().cols):
                row.append([0] * self.channels_in_pixel)
            new_items.append(row)

        matrix.set_all(new_items)

        return True

    def set_item(self, matrix, i, j, value, debug = False):
        if debug:
            print("Verbosing", i, j, "with value =", value, "having", matrix.get_size().rows, matrix.get_size().cols)
        if len(value) != self.channels_in_pixel:
            raise NameError("WrongChannelsCount")
        #   Limita a range possível de acordo com o tamanho da matriz
        if 0 <= j < matrix.get_size().cols and 0 <= i < matrix.get_size().rows:
            matrix.get_all()[i][j] = value
            return True

        raise NameError("IndexOutOfRange")
        return False

    def add(self, matrix, added_matrix):
        if matrix.get_size().rows != added_matrix.get_size().rows or matrix.get_size().cols != added_matrix.get_size().cols:
            print("Impossível adicionar: matrizes de tamanhos diferentes!")
            return False

        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                added_pixel = added_matrix.get_item(i, j)
                # Varre cada canal do pixel
                for channel in range(self.channels_in_pixel):
                    if pixel[channel] + added_pixel[channel] >= matrix.get_limit():
                        pixel[channel] = matrix.get_limit()
                    else:
                        pixel[channel] = pixel[channel] + added_pixel[channel]
                matrix.set_item(i, j, pixel)

        return True

    def sub(self, matrix, subtracted_matrix):
        if matrix.get_size().rows != subtracted_matrix.get_size().rows or matrix.get_size().cols != subtracted_matrix.get_size().cols:
            print("Impossível subtrair: matrizes de tamanhos diferentes!")
            return False

        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                subtracted_pixel = subtracted_matrix.get_item(i, j)
                # Varre cada canal do pixel
                for channel in range(self.channels_in_pixel):
                    print(pixel[channel], subtracted_pixel[channel])
                    if pixel[channel] - subtracted_pixel[channel] <= 0:
                        pixel[channel] = 0
                    else:
                        pixel[channel] = pixel[channel] - subtracted_pixel[channel]
                matrix.set_item(i, j, pixel)

        return True

    def noise(self, matrix):
        """ Preenche a matriz com valores aleatórios """
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = []
                # Varre cada canal do pixel
                for channel in range(self.channels_in_pixel):
                    pixel.append((int(random.randint(0, matrix.get_limit()))))
                matrix.set_item(i, j, pixel)

        return True

    def lighten(self, matrix, ammount):
        """ Clareia a imagem de acordo com o valor de ammount """
        has_image_loss = False
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                # Varre cada canal do pixel
                for channel in range(self.channels_in_pixel):
                    pixel[channel] += ammount
                    if pixel[channel] > matrix.get_limit():
                        has_image_loss = True
                        pixel[channel] = matrix.get_limit()
                matrix.set_item(i, j, pixel)
        if has_image_loss:
            print("Possível perda de definição da imagem.")

        return True

    def darken(self, matrix, ammount):
        """ Escurece a imagem de acordo com o valor de ammount """
        has_image_loss = False
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                # Varre cada canal do pixel
                for channel in range(self.channels_in_pixel):
                    pixel[channel] -= ammount
                    if pixel[channel] < 0:
                        has_image_loss = True
                        pixel[channel] = 0
                matrix.set_item(i, j, pixel)
        if has_image_loss:
            print("Possível perda de definição da imagem.")

        return True

    def invert(self, matrix):
        """ Inverte as cores de imagem """
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                # Varre cada canal do pixel
                for channel in range(self.channels_in_pixel):
                    pixel[channel] = matrix.get_limit() - pixel[channel]
                matrix.set_item(i, j, pixel)

        return True

    def black_and_white(self, matrix):
        print("HA! IT WAS NEVER IMPLEMENTED FOR COLORED PPM IMAGES! SURPRISE!!!!")
        return False

    def decompose(self, matrix, matrix_template):
        """ Decompõe os canais de uma imagem PPM em imagens PGM """
        channels = []
        for i in range(self.channels_in_pixel):
            channels.append(copy.deepcopy(matrix_template))
        for channel in channels:
            channel.set_format('P2')
            channel.set_limit(matrix.get_limit())
            channel.set_size(matrix.get_size().rows, matrix.get_size().cols)

        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = matrix.get_item(i, j)
                for c in range(self.channels_in_pixel):
                    channels[c].set_item(i, j, pixel[c])

        filename = re.findall("(.+)\.\w+$", matrix.get_filename())[0]
        rgb = ['B', 'G', 'R']
        for channel in channels:
            channel.write_to_file(filename + rgb.pop() + ".pgm")

    def compose_from_pgm(self, matrix, matrix_r, matrix_g, matrix_b):
        if not (matrix_r.get_size().rows == matrix_g.get_size().rows == matrix_b.get_size().rows) or not (matrix_r.get_size().cols == matrix_g.get_size().cols == matrix_b.get_size().cols):
            print("Imagens PGM são de tamanhos diferentes!")

        matrix.set_format('P3')
        matrix.set_limit(matrix_r.get_limit())
        matrix.set_size(matrix_r.get_size().rows, matrix_r.get_size().cols)
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                pixel = [matrix_r.get_item(i, j), matrix_g.get_item(i, j), matrix_b.get_item(i, j)]
                matrix.set_item(i, j, pixel)

        print("new PPM composed from " + matrix_r.get_filename() + ", " + matrix_g.get_filename() + ", " + matrix_b.get_filename() + ".")
        print("call write_to_file() to save it")

    def from_template(self, matrix, data):
        """ Carrega a matrix com os dados do template """
        i = j = 0
        pixel = []
        for element in data:
            if len(pixel) == self.channels_in_pixel:
                matrix.set_item(i, j, pixel)
                if j == matrix.get_size().cols - 1:
                    i += 1
                    j = 0
                else:
                    j += 1

                pixel = []
            pixel.append(int(element))
