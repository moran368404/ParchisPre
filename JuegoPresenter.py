from Juego import Juego
from PyQt5.QtWidgets import QMainWindow
from Jugador import Jugador
from VistaJuego import DialogDatosJugador
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton
from DialogTiradaInicial import DialogTiradaInicial


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

        # Tirada inicial para elegir jugador inicial
        dialog_tirada = DialogTiradaInicial(self.juego.jugadores)
        if dialog_tirada.exec_() == QDialog.Accepted:
            ganador = dialog_tirada.get_ganador()
            if ganador:
                # Poner el turno_actual al índice del ganador
                self.juego.turno_actual = self.juego.jugadores.index(ganador)
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

    def get_fichas(self):
        fichas = []
        for joueur in self.juego.jugadores:
            fichas.extend(joueur.fichas)
        return fichas

    def move_active_pion(self, valor_dado):
        jugador = self.juego.get_jugador_activo()
        ficha = None

        # Si el dado es 5, prioriza sacar ficha de la base automáticamente
        if valor_dado == 5:
            for f in jugador.fichas:
                if f.posicion == -1 and f.puede_moverse(valor_dado):
                    ficha = f
                    break
        # Si no hay ficha en base para sacar, mueve la primera que pueda moverse normalmente
        if ficha is None:
            for f in jugador.fichas:
                if f.posicion >= 0 and f.puede_moverse(valor_dado):
                    ficha = f
                    break

        if ficha:
            message = ficha.mover(valor_dado, self.juego.tablero)
            if message:
                self.vista.mostrar_mensaje(message)
        else:
            self.vista.mostrar_mensaje(f"No se puede mover ninguna ficha para {jugador.nombre}.")

        # Cambio de turno (excepto si es 6)
        if valor_dado != 6:
            self.juego.siguiente_turno()

        self.mostrar_turno()

    def move_ficha_directa(self, ficha, valor_dado):
        message = ficha.mover(valor_dado, self.juego.tablero)
        if message:
            self.vista.mostrar_mensaje(message)
        if valor_dado != 6:
            self.juego.siguiente_turno()
        self.mostrar_turno()


    def actualizar_tablero(self):
        self.limpia_iconos()
        self.mostrar_fichas()

    def limpia_iconos(self):
        colores = ["Rojo", "Verde", "Azul", "Amarillo"]
        for i in range(1, 69):  # casilla1 à casilla68
            nom = f"casilla{i}"
            bouton = self.vista_tablero.findChild(QPushButton, nom)
            if bouton:
                bouton.setIcon(QIcon())

        for color in colores:
            for i in range(1,8):
                nom = f"final{color}{i}"
                bouton = self.vista_tablero.findChild(QPushButton, nom)
                if bouton:
                    bouton.setIcon(QIcon())

    def mostrar_fichas(self):
        for jugador in self.juego.jugadores:
            for ficha in jugador.fichas:
                zona = ficha.zona
                if zona == 'tablero':
                    self.mostrar_ficha_tablero(ficha, jugador)
                elif zona == 'pasillo':
                    self.mostrar_ficha_pasillo(ficha, jugador)
                elif zona == 'meta':
                    self.mostrar_ficha_meta(ficha, jugador)
                
                
    
    def mostrar_ficha_pasillo(self, ficha, jugador):
        index = ficha.posicion
        nom_casilla = f"final{jugador.color.capitalize()}{index}"
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

    def mostrar_ficha_tablero(self, ficha, jugador):
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

    def mostrar_ficha_meta(self, ficha, jugador):
        nom_casilla = f"llegada{jugador.color.capitalize()}"
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
