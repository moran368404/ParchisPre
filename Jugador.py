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
        self.color = color  # Color de las fichas del jugador
        self.fichas = [Ficha(i, -1, None, self) for i in range(4)]

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
        self.jugador = jugador  # la pieza pertenece a este jugador
        self.zona = 'salida'

    def obtener_posicion_salida(self) -> int:
        color = self.jugador.color.lower()
        if color == "rojo":
            return 38 - 1
        elif color == "amarillo":
            return 4 - 1
        elif color == "azul":
            return 21 - 1
        elif color == "verde":
            return 55 - 1
        else:
            return 0

    def mover(self, pasos: int, tablero):
        if not self.puede_moverse(pasos):
            return f"Ficha {self.id} de {self.jugador.nombre} no puede moverse."

        if self.zona == 'salida':
            nueva_posicion = self.obtener_posicion_salida()
            self.zona = 'tablero'
        elif self.zona == 'tablero':
            nueva_posicion = (self.posicion + pasos) % 68
            if self.ha_entrado_a_pasillo(self.posicion, nueva_posicion):
                self.zona = 'pasillo'
                nueva_posicion = 1
            else:
                premio = self.capturar(tablero, nueva_posicion)
                if premio > 0:
                    nueva_posicion = (nueva_posicion + premio) % 68
                    if self.ha_entrado_a_pasillo(self.posicion, nueva_posicion):
                        self.zona = 'pasillo'
                        nueva_posicion = 1
        elif self.zona == 'pasillo':
            nueva_posicion = self.posicion + pasos
            if self.ha_llegado_a_meta(nueva_posicion):
                self.zona = 'meta'
            
            
        nueva_casilla = tablero.obtener_casilla(nueva_posicion, self.zona, self.jugador.color.lower())
        

        if self.casilla_actual:
            self.casilla_actual.quitar_ficha(self)
        self.posicion = nueva_posicion
        self.casilla_actual = nueva_casilla

        nueva_casilla.agregar_ficha(self)

        # return f"Ficha {self.id} de {self.jugador.nombre} desplazada a la posición {self.posicion}."

    def capturar(self, tablero, nueva_posicion: int):
        casilla = tablero.obtener_casilla(nueva_posicion, 'tablero', self.jugador.color.lower())
        if tablero.es_casilla_especial(nueva_posicion):
            return 0
        ha_capturado = False
        for ficha in casilla.fichas:
            if ficha.zona == 'tablero' and (ficha.jugador.color != self.jugador.color):
                ha_capturado = True
                ficha.zona = 'salida'
                ficha.posicion = -1
        return 20 if ha_capturado else 0

    def ha_entrado_a_pasillo(self, vieja_posicion: int, nueva_posicion: int):
        color = self.jugador.color.lower()
        if color == 'rojo':
            return nueva_posicion > 33 and (33 >= vieja_posicion > 6)
        elif color == 'amarillo':
            return nueva_posicion >= 0 and (67 >= vieja_posicion > 40)
        elif color == 'azul':
            return nueva_posicion > 16 and ((16 >= vieja_posicion > 0) or (vieja_posicion > 58))
        elif color == 'verde':
            return nueva_posicion > 50 and (50 >= vieja_posicion > 23)

    def ha_llegado_a_meta(self, nueva_posicion: int):
        return nueva_posicion >= 8

    def puede_moverse(self, pasos: int) -> bool:
        """
        Comprueba si la ficha puede moverse:
        - Debe estar en la pista (aún no en la meta).
        - El número de pasos no supera el final de la pista.
        - No sale de la meta."""

        if isinstance(self.casilla_actual, CasillaMeta):
            return False

        if self.posicion == -1:
            return pasos == 5

        if self.posicion >= 0:
            return True
        return False
