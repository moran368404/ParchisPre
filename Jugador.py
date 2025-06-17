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
        self.fichas = [Ficha(i, -1, Casilla(0), self) for i in range(4)]     # Lista de fichas del jugador (List[Ficha])

    def fichas_en_meta(self) -> bool:
        """
        Devuelve True si al menos una ficha ha llegado a la meta.
        """
        for ficha in self.fichas:
            if isinstance(ficha.casilla_actual, CasillaMeta):
                return True
        return False

    def get_ficha_active(self, pasos):
        # Prioridad a las fichas que ya están en el tablero
        for ficha in self.fichas:
            if ficha.posicion >= 0 and ficha.puede_moverse(pasos):
                return ficha

        # Entonces intentamos sacar uno si el dado es 6
        for ficha in self.fichas:
            if ficha.posicion == -1 and ficha.puede_moverse(pasos):
                return ficha

        return None

class Ficha:
    """
    Representa una ficha individual de un jugador.
    Cada ficha tiene un identificador único, una posición actual en el tablero (casilla),
    y mantiene un enlace a su casilla actual (objeto de typo Casilla).
    La clase permite mover la ficha, comprobar si puede moverse una cantidad de pasos determinada
    según las reglas del juego."""
    
    def __init__(self, id: int, posicion: int, casilla_actual, jugador: Jugador):
        self.id = id
        self.posicion = posicion
        self.casilla_actual = casilla_actual  # objeto de typo Casilla
        self.jugador = jugador # la pieza pertenece a este jugador

    def obtener_posicion_salida(self) -> int:
        color = self.jugador.color.lower()
        if color == "amarillo":
            return 0
        elif color == "azul":
            return 17
        elif color == "rojo":
            return 34
        elif color == "verde":
            return 51
        else:
            return 0

    def mover(self, pasos: int, tablero):
        if not self.puede_moverse(pasos):
            return f"Ficha {self.id} de {self.jugador.nombre} no puede moverse."

        if self.posicion == -1 and pasos == 6:
            nueva_posicion = self.obtener_posicion_salida()
        else:
            nueva_posicion = (self.posicion + pasos) % 68

        nueva_casilla = tablero.obtener_casilla(nueva_posicion)

        if self.casilla_actual:
            self.casilla_actual.quitar_ficha(self)

        self.posicion = nueva_posicion
        self.casilla_actual = nueva_casilla

        nueva_casilla.agregar_ficha(self)

        # Aquí, puede llamar a capturar_ficha SÓLO si hay otro archivo presente.
        for ficha in nueva_casilla.fichas[:]:  # Copia para evitar modificaciones durante el bucle
            if ficha.jugador != self.jugador:
                tablero.capturar_ficha(ficha)

        #return f"Ficha {self.id} de {self.jugador.nombre} desplazada a la posición {self.posicion}."


    def puede_moverse(self, pasos: int) -> bool:
        """
        Comprueba si la ficha puede moverse:
        - Debe estar en la pista (aún no en la meta).
        - El número de pasos no supera el final de la pista.
        - No sale de la meta."""

        if isinstance(self.casilla_actual, CasillaMeta):
            return False

        if self.posicion == -1:
            return pasos == 6

        if self.posicion >= 0:
            return True

        return False