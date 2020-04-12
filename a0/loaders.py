from abc import ABC, abstractmethod
import re


class ImageLoaderInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def load(self, filename):
        pass

    @abstractmethod
    def write(self, filename):
        pass


class PGMLoader(ImageLoaderInterface):

    def __init__(self):
        pass

    def write(self, matrix, filename):
        """ Salva os dados de um arquivo .pgm """
        print("Saving", filename, "as PGM")
        with open(filename, "w") as file:
            file.write(str(matrix.get_format()) + "\n")
            file.write(str(matrix.get_size().cols) + "\n")
            file.write(str(matrix.get_size().rows) + "\n")
            file.write(str(matrix.get_limit()))
            for i in range(matrix.get_size().rows):
                file.write("\n")
                for j in range(matrix.get_size().cols):
                    file.write(str(matrix.get_item(i, j)))
                    if (j < matrix.get_size().cols - 1):
                        file.write(" ")

    def load(self, filename):
        """ Carrega os dados de um arquivo .pgm e retorna uma lista com o conteúdo relevante """
        print("Loading", filename, "as PGM")
        data = []
        # TODO: fazer isso direito
        matrix_template = {
            'format': '',
            'width': 0,
            'height': 0,
            'limit': False,
            'data': []
        }
        with open(filename, "r") as file:
            for line in file:
                content = re.split('\s', line)
                for element in content:
                    if element == '#':
                        break
                    if element == "":
                        continue
                    data.append(element)

        matrix_template['format'] = data.pop(0)
        matrix_template['width'] = data.pop(0)
        matrix_template['height'] = data.pop(0)
        matrix_template['limit'] = data.pop(0)
        matrix_template['data'] = data

        return matrix_template
