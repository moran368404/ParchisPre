from Casilla import Casilla


class CasillaSegura(Casilla):
    """""""""
    Es una de las herencias de casilla, esta clase representa cuando una casilla es "Segura" de comer,
    significa que otro jugador no puede comerse una casilla de un jugador "enemigo" si su ficha se
    encuentra en una de estas casillas
    """""""""

    def __init__(self, posicion: int):
        super().__init__(posicion)
        self.es_segura = True
