class Casilla:
    """""""""
    En el constructor definimos que cada casilla tiene un numero de posición y
    una lista de fichas que físicamente sería la cantidad de fichas que tiene
    simultáneamente.
    
    def agregar_ficha: Agrega una ficha a la lista de fichas de la casilla
    def quitar_ficha: Saca a una ficha de la lista de fichas de la casilla
    """""""""
    def __init__(self, posicion: int):
        self.posicion = posicion
        self.fichas: List[Ficha] = []

    def agregar_ficha(self, ficha: 'Ficha'):
        self.fichas.append(ficha)

    def quitar_ficha(self, ficha: 'Ficha'):
        if ficha in self.fichas:
            self.fichas.remove(ficha)