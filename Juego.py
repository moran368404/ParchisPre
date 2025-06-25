from typing import List
from typing import Optional
from Jugador import Jugador
from Jugador import Ficha
from Tablero import Tablero
from Dado import Dado


class Juego:
    def __init__(self):
        self.jugadores: List[Jugador] = []
        self.tablero = Tablero()
        self.dado = Dado(6)
        self.turno_actual = 0
        self.num_jugadores = 0
        self.ultimo_resultado_dado = 0

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    def get_jugador_activo(self):
        return self.jugadores[self.turno_actual]


if __name__ == '__main__':
    pass
