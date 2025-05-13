from Juego import Juego
from VistaJuego import VistaJuego
from Jugador import Jugador

class JuegoPresenter:

    def __init__(self, vista: VistaJuego, juego: Juego):
        self.vista = vista
        self.juego = juego

    def mostrar_instrucciones(self):
        instructions = "Las reglas del Parchís..."
        self.vista.mostrar_mensaje(instructions)

    def configurar_jugadores(self, cantidad):
        self.juego.configurar_jugadores(cantidad)
        self.iniciar()

    def iniciar(self):
        self.juego.iniciar_juego()
        self.vista.mostrar_mensaje("Juego iniciado!")

    def lanzar_dado(self):
        resultado = self.juego.lanzar_dado()
        self.vista.mostrar_dado(resultado)
        return resultado

    def mover_ficha(self, jugador: Jugador, ficha_id: int, pasos: int):
        ficha = jugador.fichas[ficha_id]
        if ficha.puede_moverse(pasos):
            self.juego.mover_ficha(jugador, ficha, pasos)
            self.vista.mostrar_mensaje(f"{jugador.nombre} mueve ficha {ficha_id} a {ficha.posicion}")
            self.vista.mostrar_tablero(self.juego.tablero)
            ganador = self.juego.verificar_ganador()
            if ganador:
                self.vista.mostrar_mensaje(f"{ganador.nombre} ha ganado!")
                return True
            else:
                self.juego.siguiente_turno()
        else:
            self.vista.mostrar_mensaje("Movimiento inválido")
        return False