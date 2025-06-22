from Juego import Juego
from PyQt5.QtWidgets import QMainWindow
from Jugador import Jugador
from VistaJuego import DialogDatosJugador
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton

class JuegoPresenter:
    def __init__(self, vista_principale, juego):
        self.vista = vista_principale
        self.juego = juego

        self.vista_inicio = None
        self.vista_parchis = None
        self.vista_jugadores = None
        self.vista_tablero = None

        self.colores_disponibles = ["rojo", "verde", "amarillo", "azul"]

    def configurar_jugadores(self, cantidad):
        self.juego.num_jugadores = cantidad
        for i in range(cantidad):
            dialog = DialogDatosJugador(self.colores_disponibles)
            resultado = dialog.exec_()
            if resultado == QDialog.Accepted:
                nombre, color = dialog.get_datos()
                if color in self.colores_disponibles:
                    self.colores_disponibles.remove(color)
                    jugador = Jugador(nombre, color)
                    self.juego.jugadores.append(jugador)
                else:
                    self.mostrar_mensaje("Color ya cogido. Ignorado.")

            else:
                self.mostrar_mensaje("Cancelado.")
                return

        self.iniciar()


    def iniciar(self):
        self.vista.close()
        if self.vista_tablero:
            self.vista_tablero.show()
            self.actualizar_tablero()
            self.mostrar_turno()


    def mostrar_instrucciones(self):
        instructions = "El Parchís es un juego de mesa tradicional que se juega entre dos y cuatro personas. Cada jugador tiene cuatro fichas de un color (amarillo, rojo, azul o verde) y el objetivo del juego es llevar todas sus fichas desde la salida hasta la meta antes que los demás jugadores. Cada jugador comienza con sus fichas en la 'casa', y para sacar una ficha al tablero debe obtener un seis al lanzar el dado. Al sacar un seis, el jugador puede sacar una ficha o mover una que ya esté en juego seis casillas hacia adelante. Además, al sacar un seis se gana un turno extra. Las fichas avanzan en sentido contrario a las agujas del reloj alrededor del tablero, siguiendo un camino común de 68 casillas. Cada jugador tiene una casilla de entrada a su recorrido final: el amarillo entra por la casilla 1, el azul por la 18, el rojo por la 35 y el verde por la 52. Desde ahí, las fichas deben recorrer un camino final de siete casillas de su color hasta llegar a la meta. Para entrar en la meta, la ficha debe avanzar exactamente el número de pasos necesarios; de lo contrario, no puede moverse. Si una ficha cae en una casilla ocupada por una ficha de otro jugador (y dicha casilla no es segura), la ficha rival es capturada y enviada de regreso a su casa. El juego continúa hasta que uno de los jugadores logra llevar sus cuatro fichas a la meta, momento en el cual es declarado ganador."
        self.vista.mostrar_mensaje(instructions)

    def mostrar_turno(self):
        jugador = self.juego.get_jugador_activo()
        self.vista_tablero.mostrar_turno(jugador.nombre, jugador.color)


    """def lanzar_dado(self):
        resultado = self.juego.lanzar_dado()
        self.vista.mostrar_dado(resultado)
        return resultado"""

    """def mover_ficha(self, jugador: Jugador, ficha_id: int, pasos: int):
        ficha = jugador.fichas[ficha_id]
        if ficha.puede_moverse(pasos):
            self.juego.mover_ficha(jugador, ficha, pasos)
            self.vista.mostrar_mensaje(f"{jugador.nombre} mueve ficha {ficha_id} a {ficha.posicion}")
            self.actualizar_tablero()
            ganador = self.juego.verificar_ganador()
            if ganador:
                self.vista.mostrar_mensaje(f"{ganador.nombre} ha ganado!")
                return True
            else:
                self.juego.siguiente_turno()
        else:
            self.vista.mostrar_mensaje("Movimiento inválido")
        return False"""


    def get_fichas(self):
        fichas = []
        for joueur in self.juego.jugadores:
            fichas.extend(joueur.fichas)
        return fichas

    def move_active_pion(self, valor_dado):
        jugador = self.juego.get_jugador_activo()
        ficha = jugador.get_ficha_active(valor_dado)

        if ficha:
            message = ficha.mover(valor_dado, self.juego.tablero)
            if message:
                self.vista.mostrar_mensaje(message)
        else:
            self.vista.mostrar_mensaje(f"No se puede mover ningúna ficha para {jugador.nombre}.")

        # Cambio de turno (excepto si es 6)
        if valor_dado != 6:
            self.juego.siguiente_turno()

        self.mostrar_turno()

    def actualizar_tablero(self):
        self.limpia_iconos()
        self.mostrar_fichas()

    def limpia_iconos(self):
        for i in range(1, 69):  # casilla1 à casilla68
            nom = f"casilla{i}"
            bouton = self.vista_tablero.findChild(QPushButton, nom)
            if bouton:
                bouton.setIcon(QIcon())

    def mostrar_fichas(self):
        for jugador in self.juego.jugadores:
            for ficha in jugador.fichas:
                if ficha.posicion >= 0:
                    index = ficha.posicion + 1  # porque casilla1 corresponde a la posición 0
                    nom_casilla = f"casilla{index}"
                    boton = self.vista_tablero.findChild(QPushButton, nom_casilla)
                    if boton:
                        chemin_image = f"ficheros_ui/imagenes/pion_{jugador.color}.png"
                        pixmap = QPixmap(chemin_image)
                        if not pixmap.isNull():
                            icon = QIcon(pixmap)
                            boton.setIcon(icon)
                            boton.setIconSize(QSize(30, 30))
                        else:
                            print(f"Imagen no encontrada : {chemin_image}")
                    else:
                        print(f"Boton {nom_casilla} irrastreable.")

