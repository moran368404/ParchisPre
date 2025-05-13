from Ficha import Ficha
from Casilla import Casilla
from CasillaMeta import CasillaMeta

class Jugador:
    """
    Clase que representa a uno de los jugadores del juego de Parchís.
    Cada jugador tiene un nombre, un color identificativo, y un conjunto de fichas
    que controla durante la partida.
    Esta clase permite saber si el jugador tiene algunas fichas en la casilla Meta.
    """
    def __init__(self, nombre: str, color: str):
        self.nombre = nombre
        self.color = color                # Color de las fichas del jugador
        self.fichas = [Ficha(i, 0, Casilla(0)) for i in range(4)]                  # Lista de fichas del jugador (List[Ficha])

    def fichas_en_meta(self) -> bool:
        """
        Devuelve True si al menos una ficha ha llegado a la meta.
        """
        for ficha in self.fichas:
            if isinstance(ficha.casilla_actual, CasillaMeta):
                return True
        return False