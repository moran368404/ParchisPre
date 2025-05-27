from Casilla import Casilla

class CasillaMeta(Casilla):
    """""""""
    Esta casilla es una de las herencias de Casilla. Esta clase representa una de las metas de los
    jugadores, cuando los jugadores lleguen a esta casilla significa que están en una zona segura
    a la que ningún otro jugador puede acudir, cuando tenga 4 fichas dentro de la casilla meta
    significa que ha sido el ganador.
    """""""""
    def __init__(self, posicion: int):
        super().__init__(posicion)