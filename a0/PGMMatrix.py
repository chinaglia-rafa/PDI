import random
from PGMMatrixInterface import PGMMatrixInterface


class PGMMatrix(PGMMatrixInterface):


    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def str(self, matrix):
        if matrix.get_size().rows == matrix.get_size().cols == 0:
            return "Matrix is empty! (0x0)"
        s = "   Matrix is %d rows by %d cols\n\n" % (matrix.get_size().rows, matrix.get_size().cols)
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                s += " %3d" % matrix.get_item(i, j)
            s += "\n"

        return s

    def init(self, matrix):
        """ Inicializa um vetor de tamanho size x size com zeros """

        new_items = []
        for i in range(matrix.get_size().rows):
            row = []
            for j in range(matrix.get_size().cols):
                row.append(0)
            new_items.append(row)

        matrix.set_all(new_items)

        return True

    def set_item(self, matrix, i, j, value, debug = False):
        if debug:
            print("Verbosing", i, j, "with value =", value, "having", matrix.get_size().rows, matrix.get_size().cols)
        #   Limita a range possível de acordo com o tamanho da matriz
        if 0 <= j < matrix.get_size().cols and 0 <= i < matrix.get_size().rows:
            matrix.get_all()[i][j] = int(value)
            return True

        raise NameError("IndexOutOfRange")
        return False

    def add(self, matrix, added_matrix):
        if matrix.get_size().rows != added_matrix.get_size().rows or matrix.get_size().cols != added_matrix.get_size().cols:
            print("Impossível adicionar: matrizes de tamanhos diferentes!")
            return False

        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                if matrix.get_item(i, j) + added_matrix.get_item(i, j) >= matrix.get_limit():
                    matrix.set_item(i, j, matrix.get_limit())
                else:
                    matrix.set_item(i, j, matrix.get_item(i, j) + added_matrix.get_item(i, j))

        return True

    def sub(self, matrix, subtracted_matrix):
        if matrix.get_size().rows != subtracted_matrix.get_size().rows or matrix.get_size().cols != subtracted_matrix.get_size().cols:
            print("Impossível subtrair: matrizes de tamanhos diferentes!")
            return False

        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                if matrix.get_item(i, j) - subtracted_matrix.get_item(i, j) <= 0:
                    matrix.set_item(i, j, 0)
                else:
                    matrix.set_item(i, j, matrix.get_item(i, j) - subtracted_matrix.get_item(i, j))

        return True

    def noise(self, matrix):
        """ Preenche a matriz com valores aleatórios """
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                matrix.set_item(i, j, random.randint(0, matrix.get_limit()))

    def lighten(self, matrix, ammount):
        """ Clareia a imagem de acordo com o valor de ammount """
        has_image_loss = False
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                new_value_for_pixel = matrix.get_item(i, j) + ammount
                if new_value_for_pixel > matrix.get_limit():
                    has_image_loss = True
                    new_value_for_pixel = matrix.get_limit()

                matrix.set_item(i, j, new_value_for_pixel)
        if has_image_loss:
            print("Possível perda de definição da imagem.")

    def darken(self, matrix, ammount):
        """ Escurece a imagem de acordo com o valor de ammount """
        has_image_loss = False
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                new_value_for_pixel = matrix.get_item(i, j) - ammount
                if new_value_for_pixel < 0:
                    has_image_loss = True
                    new_value_for_pixel = 0

                matrix.set_item(i, j, new_value_for_pixel)
        if has_image_loss:
            print("Possível perda de definição da imagem.")

    def black_and_white(self, matrix):
        """ Transforma a Imagem em Preto e Branco """
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                if matrix.get_item(i, j) < matrix.get_limit() // 2:
                    new_value_for_pixel = 0
                else:
                    new_value_for_pixel = matrix.get_limit()

                matrix.set_item(i, j, new_value_for_pixel)
        matrix.set_limit(1)

    def invert(self, matrix):
        """ Inverte as cores de imagem """
        for i in range(matrix.get_size().rows):
            for j in range(matrix.get_size().cols):
                new_value_for_pixel = matrix.get_limit() - matrix.get_item(i, j)
                if new_value_for_pixel < 0:
                    new_value_for_pixel = matrix.get_limit()

                matrix.set_item(i, j, new_value_for_pixel)

    def from_template(self, matrix, data):
        """ Carrega a matrix com os dados do template """
        i = j = 0
        for element in data:
            matrix.set_item(i, j, element)
            if j == matrix.get_size().cols - 1:
                i += 1
                j = 0
            else:
                j += 1
