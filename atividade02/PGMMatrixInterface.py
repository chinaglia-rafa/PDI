from abc import ABC, abstractmethod


class PGMMatrixInterface(ABC):

    def __init__():
        pass

    @abstractmethod
    def init(self, matrix):
        pass

    @abstractmethod
    def str(self, matrix):
        pass

    @abstractmethod
    def set_item(self, matrix, i, j, value, debug = False):
        pass

    @abstractmethod
    def add(self, matrix, added_matrix):
        pass

    @abstractmethod
    def sub(self, matrix, subtracted_matrix):
        pass

    @abstractmethod
    def noise(self, matrix):
        pass

    @abstractmethod
    def lighten(self, matrix, ammount):
        pass

    @abstractmethod
    def darken(self, matrix, ammount):
        pass

    @abstractmethod
    def black_and_white(self, matrix):
        pass

    @abstractmethod
    def invert(self, matrix):
        pass

    @abstractmethod
    def decompose(self, matrix, matrix_template):
        pass
