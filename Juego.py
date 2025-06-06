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
        ##self.jugador_actual = self.jugadores[self.turno_actual]

    def configurar_jugadores(self, cantidad):
        self.num_jugadores = cantidad

    def iniciar_juego(self):
        colores_disponibles = ["rojo", "verde", "amarillo", "azul"]
        for i in range(self.num_jugadores):  # O cambia a 4 si vas a permitir 4 jugadores
            nombre = input(f"Ingrese el nombre del jugador {i + 1}: ")

            while True:
                color = input(f"{nombre}, elige tu color ({', '.join(colores_disponibles)}): ").lower()
                if color in colores_disponibles:
                    colores_disponibles.remove(color)
                    break
                else:
                    print("Color inválido o ya elegido. Intenta de nuevo.")

            self.jugadores.append(Jugador(nombre, color))

    def lanzar_dado(self) -> int:
        return self.dado.lanzar()

    def mover_ficha(self, jugador: Jugador, ficha: Ficha, pasos: int):
        self.tablero.mover_ficha(ficha, pasos)

    def verificar_ganador(self) -> Optional[Jugador]:
        for jugador in self.jugadores:
            if jugador.fichas_en_meta():
                return jugador
        return None

    def siguiente_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

if __name__ == '__main__':
    pass
