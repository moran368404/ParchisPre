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

    """def configurar_jugadores(self, cantidad):
        self.num_jugadores = cantidad"""

    """def iniciar_juego(self, jugadores_info):
        for nombre, color in jugadores_info:
            self.jugadores.append(Jugador(nombre, color))"""

    """def lanzar_dado(self) -> int:
        resultado = self.dado.lanzar()
        self.ultimo_resultado_dado = resultado
        return resultado"""

    """def verificar_ganador(self) -> Optional[Jugador]:
        for jugador in self.jugadores:
            if jugador.fichas_en_meta():
                return jugador
        return None"""

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    def get_jugador_activo(self):
        return self.jugadores[self.turno_actual]


if __name__ == '__main__':
    pass
