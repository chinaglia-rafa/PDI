import random
from ImageLoader import ImageLoader


class Size:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols


class Matrix:

    def __init__(self, rows = 0, cols = 0):
        self.__items = []
        self.__size = Size(rows, cols)
        self.__limit = False
        self.__format = ''
        self.init()

    def init(self):
        """ Inicializa um vetor de tamanho size x size com zeros """

        for i in range(self.__size.rows):
            row = []
            for j in range(self.__size.cols):
                row.append(0)
            self.__items.append(row)

        return True

    def __str__(self):
        if self.__size.rows == self.__size.cols == 0:
            return "Matrix is empty! (0x0)"
        s = "   Matrix is %d rows by %d cols\n\n" % (self.__size.rows, self.__size.cols)
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                s += " %3d" % self.__items[i][j]
            s += "\n"

        return s

    def get_all(self):
        """ Retorna todo o vetor de itens """
        return self.__items

    def get_limit(self):
        return self.__limit

    def set_limit(self, value):
        self.__limit = int(value)

    def get_format(self):
        return self.__format

    def set_format(self, value):
        self.__format = value

    def get_item(self, i, j):
        #   Limita a range possível de acordo com o tamanho da matriz
        if 0 <= j < self.__size.cols and 0 <= i < self.__size.rows:
            return self.__items[i][j]

        return False


    def set_item(self, i, j, value, debug = False):
        #   Limita a range possível de acordo com o tamanho da matriz
        if debug:
            print("Verbosing", i, j, "with value =", value, "having", self.__size.rows, self.__size.cols)
        if 0 <= j < self.__size.cols and 0 <= i < self.__size.rows:
            self.__items[i][j] = int(value)
            return True

        raise NameError("IndexOutOfRange")
        return False

    def get_size(self):
        return self.__size

    def add(self, matrix):
        if self.__size.rows != matrix.get_size().rows or self.__size.cols != matrix.get_size().cols:
            print("Impossível adicionar: matrizes de tamanhos diferentes!")
            return False

        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                if self.get_item(i, j) + matrix.get_item(i, j) >= 100:
                    self.set_item(i, j, 100)
                else:
                    self.set_item(i, j, self.get_item(i, j) + matrix.get_item(i, j))

        return True

    def sub(self, matrix):
        if self.__size.rows != matrix.get_size().rows or self.__size.cols != matrix.get_size().cols:
            print("Impossível subtrair: matrizes de tamanhos diferentes!")
            return False

        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                if self.get_item(i, j) - matrix.get_item(i, j) <= 0:
                    self.set_item(i, j, 0)
                else:
                    self.set_item(i, j, self.get_item(i, j) - matrix.get_item(i, j))

        return True

    def noise(self):
        """ Preenche a matriz com valores aleatórios """
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                self.set_item(i, j, random.randint(0, 100))

    def lighten(self, ammount):
        """ Clareia a imagem de acordo com o valor de ammount """
        has_image_loss = False
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                new_value_for_pixel = self.get_item(i, j) + ammount
                if new_value_for_pixel > self.__limit:
                    has_image_loss = True
                    new_value_for_pixel = self.__limit

                self.set_item(i, j, new_value_for_pixel)
        if has_image_loss:
            print("Possível perda de definição da imagem.")

    def darken(self, ammount):
        """ Escurece a imagem de acordo com o valor de ammount """
        has_image_loss = False
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                new_value_for_pixel = self.get_item(i, j) - ammount
                if new_value_for_pixel < 0:
                    has_image_loss = True
                    new_value_for_pixel = 0

                self.set_item(i, j, new_value_for_pixel)
        if has_image_loss:
            print("Possível perda de definição da imagem.")

    def black_and_white(self):
        """ Transforma a Imagem em Preto e Branco """
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                if self.get_item(i, j) < self.get_limit() // 2:
                    new_value_for_pixel = 0
                else:
                    new_value_for_pixel = self.get_limit()

                self.set_item(i, j, new_value_for_pixel)
        self.set_limit(1)

    def contrast(self, ammount):
        """ Altera o contraste da imagem """
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                if self.get_item(i, j) < self.get_limit() // 2:
                    if self.get_item(i, j) - ammount < 0:
                        new_value_for_pixel = 0
                    else:
                        new_value_for_pixel = self.get_item(i, j) - ammount
                else:
                    if self.get_item(i, j) + ammount > self.get_limit():
                        new_value_for_pixel = self.get_limit()
                    else:
                        new_value_for_pixel = self.get_item(i, j) + ammount


                self.set_item(i, j, new_value_for_pixel)

    def invert(self):
        """ Inverte as cores de imagem """
        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                new_value_for_pixel = self.__limit - self.get_item(i, j)
                if new_value_for_pixel < 0:
                    new_value_for_pixel = self.__limit

                self.set_item(i, j, new_value_for_pixel)

    def rotate(self):
        """ Rotaciona a imagem 90 graus no sentido horário """
        # TODO: criar uma instância melhor de Matrix()
        new_matrix = Matrix(self.__size.cols, self.__size.rows)
        new_matrix.set_format(self.__format)
        if self.__limit:
            new_matrix.set_limit(self.__limit)

        for i in range(self.__size.rows):
            for j in range(self.__size.cols):
                new_matrix.set_item(j, self.__size.rows - 1 - i, self.get_item(i, j))

        self.__size.cols, self.__size.rows = new_matrix.get_size().cols, new_matrix.get_size().rows
        self.__items = new_matrix.get_all()

    def load_from_file(self, filename):
        """ Carrega os dados de um arquivo usando o loader strategy designado """

        loader = ImageLoader()
        loader.load(self, filename)

    def write_to_file(self, filename):
        """ Salva os dados em um arquivo usando o loader strategy designado """

        loader = ImageLoader()
        loader.write(self, filename)

    def from_template(self, matrix_template):
        """
            Atualiza uma matriz com dados de uma matriz modelo no formato
            matrix_template = {
                'format': '',
                'width': 0,
                'height': 0,
                'limit': False,
                'data': []
            }
        """
        self.set_format(matrix_template['format'])
        if matrix_template['limit']:
            self.set_limit(matrix_template['limit'])
        self.get_size().rows = int(matrix_template['height'])
        self.get_size().cols = int(matrix_template['width'])

        i = j = 0
        # zera a situação da Matrix
        self.init()
        for element in matrix_template['data']:
            self.set_item(i, j, element)
            if j == self.get_size().cols - 1:
                i += 1
                j = 0
            else:
                j += 1
