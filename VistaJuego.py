from Tablero import Tablero
from Dado import Dado
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel, QWidget
from ui_parchis_para_pc import Ui_MainWindow as UiParchisMainWindow
from ui_tablero import Ui_MainWindow as UiTableroMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QPixmap


class VistaBase(QMainWindow):
    def mostrar_mensaje(self, mensaje: str):
        if hasattr(self.ui, 'mensajes'):
            self.ui.mensajes.setText(mensaje)
        else:
            QMessageBox.information(self, "Mensaje", mensaje)


# --- Clase de interfaz Parchis (ui_parchis_para_pc) ---
class VistaParchis(VistaBase):
    def __init__(self, presenter=None):
        super().__init__()
        self.ui = UiParchisMainWindow()
        self.ui.setupUi(self)
        self.presenter = presenter

        # Conexiones de botones sólo si el presentador está definido
        if self.presenter:
            self.ui.btnJugar.clicked.connect(self.abrir_numero_jugadores)
            self.ui.btnInstrucciones.clicked.connect(self.presenter.mostrar_instrucciones)
            self.ui.btnSalir.clicked.connect(self.cerrar)

    def conectar_senales(self, presenter):
        self.presenter = presenter
        self.ui.btnJugar.clicked.connect(self.abrir_numero_jugadores)
        self.ui.btnInstrucciones.clicked.connect(self.presenter.mostrar_instrucciones)
        self.ui.btnSalir.clicked.connect(self.cerrar)

    def abrir_numero_jugadores(self):
        self.ventana_jugadores = VentanaJugadores(self.presenter)
        self.close()
        self.ventana_jugadores.show()

    def cerrar(self):
        self.close()
        exit()

    def mostrar_tablero(self, tablero: Tablero):
        self.mostrar_mensaje("\nTablero:")
        for i, casilla in enumerate(tablero.casillas):
            if casilla.fichas:
                fichas_info = ', '.join(f"Ficha {f.id} ({f.jugador.nombre})" for f in casilla.fichas)
                self.mostrar_mensaje(f"Casilla {i}: {fichas_info}")


    def actualizar_tablero(self):
        pass


# --- Clase para la interfaz Tablero (ui_tablero) ---

class VistaTablero(VistaBase):
    def __init__(self, presenter=None):
        super().__init__()
        uic.loadUi("tablero.ui", self)
        self.presenter = presenter
        self.dado = Dado(6)
        self.labels_fichas = []
        self.tamaño_casilla = 40

        self.color_map = {
            "rojo": QColor(255, 0, 0),
            "verde": QColor(0, 255, 0),
            "amarillo": QColor(255, 255, 0),
            "azul": QColor(0, 0, 255)
        }

        self.btnLanzarDado.clicked.connect(self.lancer_de)

    def mostrar_pion_en_casilla(self, numero_casilla, color_pion):
        casilla_btn = getattr(self.vista_tablero, f"casilla{numero_casilla}", None)
        if casilla_btn:
            icon_path = f"pion_{color_pion}.png"
            icon = QIcon(QPixmap(icon_path).scaled(30, 30))
            casilla_btn.setIcon(icon)
            casilla_btn.setIconSize(casilla_btn.size())
        else:
            print(f"Casilla {numero_casilla} no encontrada.")

    def limpiar_casilla(self, numero_casilla):
        casilla_btn = getattr(self.vista_tablero, f"casilla{numero_casilla}", None)
        if casilla_btn:
            casilla_btn.setIcon(QIcon())
            casilla_btn.setStyleSheet("")


    def set_presenter(self, presenter):
        self.presenter = presenter
        self.init_pions()


    def lancer_de(self):
        resultado = self.dado.lanzar()
        self.labelResultadoDado.setText(str(resultado))
        self.presenter.deplacer_pion_actif(resultado)
        self.presenter.actualizar_tablero()

    def init_pions(self):
        """
        Muestra todas las fichas al principio.
        """
        fichas = self.presenter.get_fichas()  # recupera la lista de fichas
        for ficha in fichas:
            label = QLabel(self.plateau)  # Widget Añadir al tablero
            label.setText("●")  # O una imagen
            label.resize(20, 20)
            self.labels_fichas.append((ficha, label))
        self.mettre_a_jour_pions()


    def mettre_a_jour_pions(self):
        """
        Actualiza visualmente la posición de las fichas en el tablero.
        """
        for ficha, label in self.labels_fichas:
            pos_logique = ficha.position  # o la propiedad que indica la posición en el tablero
            x, y = self.position_to_coords(pos_logique)  # convierte la posición lógica en coordenadas en la interfaz
            label.move(x, y)
            label.show()

    def position_to_coords(self, pos):
        # Suponga que su tablero tiene una cuadrícula de 10x10, cada cuadrado es de 40x40 píxeles.
        case_taille = 40
        ligne = pos // 10
        colonne = pos % 10
        x = colonne * case_taille
        y = ligne * case_taille
        return x, y





    def conectar_senales(self, presenter):
        self.presenter = presenter

    def abrir_numero_jugadores(self):
        self.ventana_jugadores = VentanaJugadores(self.presenter)
        self.close()
        self.ventana_jugadores.show()

    def cerrar(self):
        self.close()
        exit()

    def mostrar_tablero(self, tablero: Tablero):
        self.mostrar_mensaje("\nTablero:")
        for i, casilla in enumerate(tablero.casillas):
            if casilla.fichas:
                fichas_info = ', '.join(f"Ficha {f.id} ({f.jugador.nombre})" for f in casilla.fichas)
                self.mostrar_mensaje(f"Casilla {i}: {fichas_info}")

    def mostrar_dado(self, resultado: int):
        self.ui.dado.setText(f"{resultado}")

    def actualizar_tablero(self):
        total_casillas = 68
        # Limpiar primero todas las casillas
        for i in range(1, total_casillas + 1):
            self.limpiar_casilla(i)

        # Afficher les pions
        for jugador in self.juego.jugadores:
            for ficha in jugador.fichas:
                if ficha.posicion >= 0:
                    index = ficha.posicion + 1  # porque casilla1 corresponde a la posición 0
                    nombre_casilla = f"casilla{index}"
                    boton = self.vista_tablero.findChild(QPushButton, nombre_casilla)

                    if boton:
                        color = ficha.color
                        pixmap = QPixmap(f"imagenes/pion_{color}.png")
                        icon = QIcon(pixmap)
                        boton.setIcon(icon)
                        boton.setIconSize(QSize(30, 30))
                    else:
                        print(f"Boton '{nombre_casilla}' irrastreable")

    def leer_input_jugador(self):
        texto = self.lineedit_pieza = QtWidgets.QLineEdit(...)
        if texto.isdigit():
            ficha_id = int(texto)
            self.presenter.mover_ficha_actual(ficha_id)
            self.ui.inputJugador.clear()
        else:
            self.mostrar_mensaje("Por favor, introduce un número válido (0-3).")

    def lanzar_dado(self):
        resultado = self.presenter.lanzar_dado()
        self.mostrar_dado(resultado)
        self.mostrar_mensaje(f"Tira el dado: {resultado}")


# --- Clase para la ventana de selección del número de jugadores ---
class VentanaJugadores(VistaBase):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        loadUi("numero_jugadores.ui", self)
        self.btn2.clicked.connect(self.elegir_2_jugadores)
        self.btn3.clicked.connect(self.elegir_3_jugadores)
        self.btn4.clicked.connect(self.elegir_4_jugadores)

    def elegir_2_jugadores(self):
        self.hide()
        QTimer.singleShot(0, lambda: self.presenter.configurar_jugadores(2))

    def elegir_3_jugadores(self):
        self.hide()
        QTimer.singleShot(0, lambda: self.presenter.configurar_jugadores(3))

    def elegir_4_jugadores(self):
        self.hide()
        QTimer.singleShot(0, lambda: self.presenter.configurar_jugadores(4))


# --- Ventana de inicio o primera ventana ---
class PrimeraVentana(VistaBase):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        loadUi("PrimeraVentana.ui", self)

from PyQt5.QtWidgets import QDialog
from formulario_jugador import Ui_DialogJugador

class DialogDatosJugador(QDialog):
    def __init__(self, colores_disponibles):
        super().__init__()
        self.ui = Ui_DialogJugador()
        self.ui.setupUi(self)
        self.ui.comboBoxCouleur.addItems(colores_disponibles)

        self.ui.btnValider.clicked.connect(self.accept)
        self.ui.btnAnnuler.clicked.connect(self.reject)

    def get_datos(self):
        return self.ui.lineEditNom.text(), self.ui.comboBoxCouleur.currentText()