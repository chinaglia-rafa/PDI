import random
from ImageLoader import ImageLoader
from PGMMatrix import PGMMatrix
from PPMMatrix import PPMMatrix


class Size:
    """Representa as dimensões da matriz que armazena os dados da imagem"""

    def __init__(self, rows = 0, cols = 0):
        self.rows = rows
        self.cols = cols


class Matrix:
    """Classe que consegue armazenar uma imagem pgm/ppm/pbm e processá-la"""

    def __init__(self, filename = ''):
        self.__filename = filename
        self.__items = []
        self.__size = Size()
        self.__limit = False
        self.__format = 'P2'

        # TODO: melhorar o valor-padrão
        self.__strategy = PGMMatrix()

        if filename != '':
            self.load_from_file(filename)
        else:
            self.__strategy.init(self)

    def __str__(self):
        return self.__strategy.str(self)

    def get_all(self):
        """ Retorna todo o vetor de itens """
        return self.__items

    def set_all(self, value):
        """ Seta o valor total para items """
        self.__items = value

    def get_limit(self):
        return self.__limit

    def get_filename(self):
        return self.__filename

    def set_limit(self, value):
        self.__limit = int(value)

    def set_filename(self, value):
        self.__filename = value

    def get_format(self):
        return self.__format

    def set_format(self, value):
        self.__format = value
        # Determina qual strategy será usada para processar a imagem
        if value == 'P2':
            self._set_strategy(PGMMatrix());
        elif value == 'P3':
            self._set_strategy(PPMMatrix());

    def get_item(self, i, j):
        #   Limita a range possível de acordo com o tamanho da matriz
        if 0 <= j < self.__size.cols and 0 <= i < self.__size.rows:
            return self.__items[i][j]

        return False


    def set_item(self, i, j, value, debug = False):
        self.__strategy.set_item(self, i, j, value, debug)

    def get_size(self):
        return self.__size

    def set_size(self, rows, cols):
        """Altera as dimensões da imagem e reseta seus dados"""
        self.__size.rows = rows
        self.__size.cols = cols
        self.__strategy.init(self)

    def _set_strategy(self, strategy):
        print("Setting image-processing strategy to", strategy)
        self.__strategy = strategy

    def add(self, matrix):
        self.__strategy.add(self, matrix)

    def sub(self, matrix):
        self.__strategy.sub(self, matrix)

    def noise(self):
        self.__strategy.noise(self)

    def lighten(self, ammount):
        self.__strategy.lighten(self, ammount)

    def darken(self, ammount):
        self.__strategy.darken(self, ammount)

    def black_and_white(self):
        self.__strategy.black_and_white(self)

    def invert(self):
        self.__strategy.invert(self)

    def decompose(self):
        #  O segundo parâmetro é o modelo de Matrix aque será usado para exportar
        self.__strategy.decompose(self, Matrix())

    def compose_from_pgm(self, m1, m2, m3):
        if self.get_format() == 'P3':
            self.__strategy.compose_from_pgm(self, m1, m2, m3)

    def rotate(self):
        """ Rotaciona a imagem 90 graus no sentido horário """
        # TODO: criar uma instância melhor de Matrix()
        new_matrix = Matrix()
        new_matrix.set_size(self.get_size().cols, self.get_size().rows)
        new_matrix.set_format(self.get_format())
        if self.get_limit():
            new_matrix.set_limit(self.get_limit())

        for i in range(self.get_size().rows):
            for j in range(self.get_size().cols):
                new_matrix.set_item(j, self.get_size().rows - 1 - i, self.get_item(i, j))

        self.set_size(new_matrix.get_size().rows, new_matrix.get_size().cols)
        self.set_all(new_matrix.get_all())

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

        # zera a situação da Matrix
        self.__strategy.init(self)
        self.__strategy.from_template(self, matrix_template['data'])
