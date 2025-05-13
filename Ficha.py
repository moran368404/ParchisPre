from CasillaMeta import CasillaMeta

class Ficha:
    """
    Representa una ficha individual de un jugador. 
    Cada ficha tiene un identificador único, una posición actual en el tablero (casilla),
    y mantiene un enlace a su casilla actual (objeto de typo Casilla).
    La clase permite mover la ficha, comprobar si puede moverse una cantidad de pasos determinada
    según las reglas del juego.
    """
    def __init__(self, id: int, posicion: int, casilla_actual):
        self.id = id
        self.posicion = posicion
        self.casilla_actual = casilla_actual  # objeto de typo Casilla


    def mover(self, pasos: int, tablero):
        """
        Desplaza la ficha varios pasos si es posible.
        - Actualiza la posición.
        - Gestionar la nueva casilla.
        - Comprobar si es necesario capturar una ficha.
        """
        if not self.puede_moverse(pasos):
            print(f"Ficha {self.id} no puede moverse.")
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

        print(f"Ficha {self.id} desplazada a la posición {self.posicion}.") # para el desarrollo


    def puede_moverse(self, pasos: int) -> bool:
        """
        Comprueba si la ficha puede moverse:
        - Debe estar en la pista (aún no en la meta).
        - El número de pasos no supera el final de la pista.
        - No sale de la meta.
        """
        if self.casilla_actual is None:
            # La ficha aún no está en juego
            return False

        if isinstance(self.casilla_actual, CasillaMeta):
            # Ya en la meta, ya no puede moverse
            return False

        # Si la ficha está en el tablero, se supone que puede moverse
        return pasos > 0
