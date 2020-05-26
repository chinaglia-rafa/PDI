from loaders import PGMLoader, PPMLoader
import re


class ImageLoader:
    """Carrega imagens pgm/ppm/pbm de acordo com sua extensão"""

    def __init__(self):
        pass

    def load(self, matrix, filename):
        loader = self.__find_strategy(filename)
        matrix_template = None
        if loader:
            matrix_template = loader.load(filename)

        matrix.from_template(matrix_template)

    def write(self, matrix, filename):
        loader = self.__find_strategy(filename)
        matrix_template = None
        if loader:
            matrix_template = loader.write(matrix, filename)

    def __find_strategy(self, filename):
        filename = filename.lower()
        ext = re.findall("\.(\w+)$", filename)
        if not ext:
            raise NameError("Malformed Filename")

        if ext[0].lower() == "pgm":
            return PGMLoader()
        elif ext[0].lower() == "ppm":
            return PPMLoader()

        raise NameError("Format Unknown")
        return None
