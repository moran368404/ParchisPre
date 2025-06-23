from typing import List
from Casilla import Casilla
from CasillaSalida import CasillaSalida
from Jugador import Ficha


class Tablero:
    def __init__(self):
        self.casillas: List[Casilla] = [Casilla(i) for i in range(68)]

    def obtener_casilla(self, posicion: int) -> Casilla:
        return self.casillas[posicion % len(self.casillas)]

    def mover_ficha(self, ficha: Ficha, pasos: int):
        return ficha.mover(pasos, self)

    def capturar_ficha(self, ficha: Ficha):
        ficha.posicion = 0
