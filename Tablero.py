from typing import List
from Casilla import Casilla
from CasillaMeta import CasillaMeta
from CasillaSalida import CasillaSalida
from Jugador import Ficha


class Tablero:
    def __init__(self):
        self.casillas: List[Casilla] = [Casilla(i) for i in range(68)]
        self.pasillo_rojo: List[Casilla] = [Casilla(i) for i in range(1, 8)]
        self.pasillo_azul: List[Casilla] = [Casilla(i) for i in range(1, 8)]
        self.pasillo_amarillo: List[Casilla] = [Casilla(i) for i in range(1, 8)]
        self.pasillo_verde: List[Casilla] = [Casilla(i) for i in range(1, 8)]
        self.casilla_meta = CasillaMeta(100)


    def obtener_casilla(self, posicion: int, zona: str, color: str) -> Casilla:
        if zona == 'pasillo':
            if color == 'rojo':
                return self.pasillo_rojo[posicion-1]
            elif color == 'amarillo':
                return self.pasillo_amarillo[posicion-1]
            if color == 'verde':
                return self.pasillo_verde[posicion-1]
            if color == 'azul':
                return self.pasillo_azul[posicion-1]
            
        elif zona == 'meta':
            return self.casilla_meta
        return self.casillas[posicion % len(self.casillas)]

    def es_casilla_especial(self, posicion):
        casillas_especiales = [ 67, 63, 54, 50, 46, 37, 33, 29, 20, 16, 12, 3]
        return posicion in casillas_especiales

    def mover_ficha(self, ficha: Ficha, pasos: int):
        return ficha.mover(pasos, self)

    def capturar_ficha(self, ficha: Ficha):
        ficha.posicion = 0
