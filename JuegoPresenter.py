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


    def mostrar_instrucciones(self):
        instructions = "Las reglas del Parchís..."
        self.vista.mostrar_mensaje(instructions)


    def lanzar_dado(self):
        resultado = self.juego.lanzar_dado()
        self.vista.mostrar_dado(resultado)
        return resultado

    def mover_ficha(self, jugador: Jugador, ficha_id: int, pasos: int):
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
        return False

    def mover_ficha_actual(self, ficha_id: int):
        jugador = self.juego.jugadores[self.juego.turno_actual]
        ficha = jugador.fichas[ficha_id]
        pasos = self.juego.ultimo_resultado_dado
        resultado = ficha.mover(pasos, self.juego.tablero)
        print("Resultado del desplazamiento:", resultado)
        self.actualizar_tablero()

    def get_fichas(self):
        fichas = []
        for joueur in self.juego.jugadores:
            fichas.extend(joueur.fichas)
        return fichas

    def deplacer_pion_actif(self, valeur_de):
        jugador = self.juego.get_jugador_activo()
        ficha = jugador.get_ficha_active(valeur_de)

        if ficha:
            message = ficha.mover(valeur_de, self.juego.tablero)
            if message:
                self.vista.mostrar_mensaje(message)
        else:
            self.vista.mostrar_mensaje(f"No se puede mover ningúna ficha para {jugador.nombre}.")

        # Cambio de turno (excepto si es 6)
        if valeur_de != 6:
            self.juego.siguiente_turno()

    def actualizar_tablero(self):
        self.nettoyer_icones()
        self.afficher_pions()

    def nettoyer_icones(self):
        for i in range(1, 69):  # casilla1 à casilla68
            nom = f"casilla{i}"
            bouton = self.vista_tablero.findChild(QPushButton, nom)
            if bouton:
                bouton.setIcon(QIcon())

    def afficher_pions(self):
        for jugador in self.juego.jugadores:
            for ficha in jugador.fichas:
                if ficha.posicion >= 0:
                    index = ficha.posicion + 1  # porque casilla1 corresponde a la posición 0
                    nom_casilla = f"casilla{index}"
                    boton = self.vista_tablero.findChild(QPushButton, nom_casilla)
                    if boton:
                        chemin_image = f"imagenes/pion_{jugador.color}.png"
                        pixmap = QPixmap(chemin_image)
                        if not pixmap.isNull():
                            icon = QIcon(pixmap)
                            boton.setIcon(icon)
                            boton.setIconSize(QSize(30, 30))
                        else:
                            print(f"Imagen no encontrada : {chemin_image}")
                    else:
                        print(f"Boton {nom_casilla} irrastreable.")

