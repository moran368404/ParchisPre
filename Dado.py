import random


class Dado:
    """""""""
    Clase Dado, en el init solamente definimos el numero de caras que tiene el dado
    también decimos que no puede contener menos de 2 y definimos la función "lanzar"
    en la que solamente busca un numero al azar entre 1 y el numero de caras definido
    en el constructor y lo retorna.
    """""""""

    def __init__(self, caras):
        if caras < 2:
            raise ValueError("Un dado debe tener al menos 2 caras.")
        self.caras = caras
        self.valor = None
        self.i = 0

    def lanzar(self):
        self.valor = random.randint(1, self.caras)
        return self.valor

    def mock_lanzar(self):
        if self.i <= 8:
            self.valor = 5
            self.i += 1
        else:
            self.valor = self.lanzar()
        return self.valor
