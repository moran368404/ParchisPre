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

    def lanzar(self):
        self.valor = random.randint(1, self.caras)
        return self.valor