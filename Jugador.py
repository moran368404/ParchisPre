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
        self.fichas = [Ficha(i, -1, Casilla(0), self) for i in range(4)]                  # Lista de fichas del jugador (List[Ficha])

    def fichas_en_meta(self) -> bool:
        """
        Devuelve True si al menos una ficha ha llegado a la meta.
        """
        for ficha in self.fichas:
            if isinstance(ficha.casilla_actual, CasillaMeta):
                return True
        return False

class Ficha:
    """
    Representa una ficha individual de un jugador.
    Cada ficha tiene un identificador único, una posición actual en el tablero (casilla),
    y mantiene un enlace a su casilla actual (objeto de typo Casilla).
    La clase permite mover la ficha, comprobar si puede moverse una cantidad de pasos determinada
    según las reglas del juego.
    """
    def __init__(self, id: int, posicion: int, casilla_actual, jugador: Jugador):
        self.id = id
        self.posicion = posicion
        self.casilla_actual = casilla_actual  # objeto de typo Casilla
        self.jugador = jugador # la pieza pertenece a este jugador#


    def mover(self, pasos: int, tablero):
        """
        Desplaza la ficha varios pasos si es posible.
        - Actualiza la posición.
        - Gestionar la nueva casilla.
        - Comprobar si es necesario capturar una ficha.
        """
        if self.puede_moverse(pasos):
            print(f"Ficha {self.id} de {self.jugador.nombre} no puede moverse.")
            return

        nueva_posicion = self.posicion + pasos
        nueva_casilla = tablero.obtener_casilla(nueva_posicion)

        # Retirar la ficha de la casilla actual
        if self.casilla_actual:
            self.casilla_actual.quitar_ficha(self)

        # Actualizar posición y casilla actual
        self.posicion = nueva_posicion
        self.casilla_actual = nueva_casilla

        # Añadir la ficha a la nueva casilla
        nueva_casilla.agregar_ficha(self)

        # Comprobar si es necesario capturar una ficha
        tablero.capturar_ficha(self)

        print(f"Ficha {self.id} de {self.jugador.nombre} desplazada a la posición {self.posicion}.") # para el desarrollo


    def puede_moverse(self, pasos: int) -> bool:
        """
        Comprueba si la ficha puede moverse:
        - Debe estar en la pista (aún no en la meta).
        - El número de pasos no supera el final de la pista.
        - No sale de la meta.
        """
        if self.posicion == -1 and pasos == 6:  # Solo puede entrar al tablero si ha sacado un 6
            return True

        if self.posicion >= 0:  # Ya se encuentra en el tablero
            return True

        if isinstance(self.casilla_actual, CasillaMeta):
            # Ya en la meta, ya no puede moverse
            return False
