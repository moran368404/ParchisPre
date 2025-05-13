from typing import List
from Casilla import Casilla
from CasillaSalida import CasillaSalida
from Ficha import Ficha

class Tablero:
    def __init__(self):
        self.casillas: List[Casilla] = [Casilla(i) for i in range(68)]

    def obtener_casilla(self, posicion: int) -> Casilla:
        return self.casillas[posicion % len(self.casillas)]

    def mover_ficha(self, ficha: Ficha, pasos: int):
        if ficha.casilla_actual:
            ficha.casilla_actual.quitar_ficha(ficha)
        ficha.mover(pasos, self)
        nueva_casilla = self.obtener_casilla(ficha.posicion)
        ficha.casilla_actual = nueva_casilla
        nueva_casilla.agregar_ficha(ficha)

    def capturar_ficha(self, ficha: Ficha):
        ficha.posicion = 0  # Regresar al inicio
    """""
    def __init__(self):
        self.casillas: List[Casilla] = self._crear_casillas()

    def _crear_casillas(self) -> List[Casilla]:
        # Crea 68 casillas como ejemplo, mezcla normales y especiales si lo necesitas
        casillas = []
        for i in range(68):
            casillas.append(Casilla(i))
        return casillas

    def obtener_siguiente_casilla(self, casilla: Casilla, pasos: int) -> Casilla:
         ###Devuelve la casilla que está a 'pasos' de la casilla actual en el tablero.
        pos_actual = casilla.posicion
        nueva_pos = (pos_actual + pasos) % len(self.casillas)
        return self.casillas[nueva_pos]

    def colocar_ficha_en_salida(self, ficha: Ficha):
        ###Coloca una ficha en su casilla de salida (según el color de su jugador).
        color = ficha.jugador.color
        # Buscar la casilla de salida correspondiente
        for casilla in self.casillas:
            if isinstance(casilla, CasillaSalida) and casilla.color == color:
                casilla.recibir_ficha(ficha)
                ficha.casilla_actual = casilla
                break
    """""