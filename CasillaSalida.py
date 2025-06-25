from Casilla import Casilla


class CasillaSalida(Casilla):
    """""
    Representa las casillas de donde los jugadores comienzan el juego, los jugadores llegan a ella cada que 
    sacan una ficha obteniendo un 5 en el dado
    """""
    def __init__(self, posicion: int):
        super().__init__(posicion)
        self.esta_activada = False

    def activar(self):
        self.esta_activada = True
