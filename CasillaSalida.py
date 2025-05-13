from Casilla import Casilla

class CasillaSalida(Casilla):
    def __init__(self, posicion: int):
        super().__init__(posicion)
        self.esta_activada = False

    def activar(self):
        self.esta_activada = True