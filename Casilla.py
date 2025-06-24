from typing import List


class Casilla:
    """
    Representa una casilla del tablero.
    Contiene su posición y una lista de fichas que están sobre ella.
    """

    def __init__(self, posicion: int):
        self.posicion = posicion
        self.fichas: List['Ficha'] = []

    def agregar_ficha(self, ficha: 'Ficha'):
        if ficha not in self.fichas:
            self.fichas.append(ficha)

    def quitar_ficha(self, ficha: 'Ficha'):
        print(ficha)
        print(self.fichas)
        if ficha in self.fichas:
            self.fichas.remove(ficha)
