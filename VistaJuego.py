from Tablero import Tablero
from Dado import Dado
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel, QWidget, QDialog
from ui_parchis_para_pc import Ui_MainWindow as UiParchisMainWindow
from ui_tablero import Ui_MainWindow as UiTableroMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QPixmap
from formulario_jugador import Ui_DialogJugador

"""class VistaBase(QMainWindow):
    def mostrar_mensaje(self, mensaje: str):
        if hasattr(self.ui, 'mensajes'):
            self.ui.mensajes.setText(mensaje)
        else:
            QMessageBox.information(self, "Mensaje", mensaje)"""


class VistaBase(QMainWindow):
    def mostrar_mensaje(self, mensaje: str):
        mensajes_label = self.findChild(QLabel, "mensajes")
        if mensajes_label:
            mensajes_label.setText(mensaje)
        else:
            QMessageBox.information(self, "Mensaje", mensaje)


# --- Clase de interfaz Parchis (ui_parchis_para_pc) ---

class VistaParchis(VistaBase):
    def __init__(self, presenter=None):
        super().__init__()
        loadUi("ficheros_ui/QtParchisParaPC.ui", self)
        # self.ui = UiParchisMainWindow()
        # self.ui.setupUi(self)
        self.presenter = presenter

        # Conexiones de botones sólo si el presentador está definido
        if self.presenter:
            self.btnJugar.clicked.connect(self.abrir_numero_jugadores)
            self.btnInstrucciones.clicked.connect(self.presenter.mostrar_instrucciones)
            self.btnSalir.clicked.connect(self.cerrar)

    def conectar_senales(self, presenter):
        self.presenter = presenter
        self.btnJugar.clicked.connect(self.abrir_numero_jugadores)
        self.btnInstrucciones.clicked.connect(self.presenter.mostrar_instrucciones)
        self.btnSalir.clicked.connect(self.cerrar)

    def abrir_numero_jugadores(self):
        self.ventana_jugadores = VentanaJugadores(self.presenter)
        self.close()
        self.ventana_jugadores.show()

    def cerrar(self):
        self.close()
        exit()

    """def mostrar_tablero(self, tablero: Tablero):
        self.mostrar_mensaje("\nTablero:")
        for i, casilla in enumerate(tablero.casillas):
            if casilla.fichas:
                fichas_info = ', '.join(f"Ficha {f.id} ({f.jugador.nombre})" for f in casilla.fichas)
                self.mostrar_mensaje(f"Casilla {i}: {fichas_info}")"""

    """def actualizar_tablero(self):
        pass"""


# --- Clase para la interfaz Tablero (ui_tablero) ---

class VistaTablero(VistaBase):
    def __init__(self, presenter=None):
        super().__init__()
        uic.loadUi("ficheros_ui/tablero.ui", self)
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

        self.btnLanzarDado.clicked.connect(self.lanzar_dado)

    """def mostrar_ficha_en_casilla(self, numero_casilla, color_pion):
        casilla_btn = getattr(self, f"casilla{numero_casilla}", None)
        if casilla_btn:
            icon_path = f"ficheros_ui/imagenes/pion_{color_pion}.png"
            icon = QIcon(QPixmap(icon_path).scaled(30, 30))
            casilla_btn.setIcon(icon)
            casilla_btn.setIconSize(casilla_btn.size())
        else:
            print(f"Casilla {numero_casilla} no encontrada.")"""

    """def limpiar_casilla(self, numero_casilla):
        casilla_btn = getattr(self, f"casilla{numero_casilla}", None)
        if casilla_btn:
            casilla_btn.setIcon(QIcon())
            casilla_btn.setStyleSheet("")"""

    def mostrar_turno(self, nombre_jugador, color_jugador):
        label_turno = self.findChild(QLabel, "label_turno")
        if label_turno:
            label_turno.setText(f"{nombre_jugador} ({color_jugador})")

    def set_presenter(self, presenter):
        self.presenter = presenter
        self.inicializar_fichas()

    def declarar_ganador(self, ganador):
        self.mostrar_mensaje(f"Tenemos un ganador: {ganador}")

    def obtener_ganador(self):
        fichas = self.presenter.get_fichas()
        fichas_en_meta = {
            'amarillo': [0, ''],
            'verde': [0, ''],
            'azul': [0, ''],
            'rojo': [0, ''],
        }
        for ficha in fichas:
            color = ficha.jugador.color.lower()
            zona = ficha.zona
            if zona == 'meta':
                fichas_en_meta[color][0] += 1
                fichas_en_meta[color][1] = ficha.jugador.nombre

        for color, en_meta in fichas_en_meta.items():
            total, nombre = en_meta
            if total >= 4:
                return nombre
        return ''

    def lanzar_dado(self):
        ganador = self.obtener_ganador()
        if ganador != '':
            self.declarar_ganador(ganador)
            return
        resultado = self.dado.lanzar()  # cambiar a mock lanzar para iniciar una partida de 2 jugadores más rápido
        self.labelResultadoDado.setText(str(resultado))
        jugador = self.presenter.juego.get_jugador_activo()
        fichas_en_base = [f for f in jugador.fichas if f.posicion == -1]
        fichas_movibles = [f for f in jugador.fichas if f.posicion >= 0 and f.puede_moverse(resultado)]
        # Si el dado es 5 y hay fichas en base Y hay fichas movibles en el tablero, preguntar al usuario si quiere sacar ficha
        if resultado == 5 and fichas_en_base and fichas_movibles:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox(self)
            msg.setWindowTitle("Sacar ficha de la base")
            msg.setText("¿Quieres sacar una ficha de la base?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            respuesta = msg.exec_()
            if respuesta == QMessageBox.Yes:
                self.presenter.move_active_pion(resultado)
                self.presenter.actualizar_tablero()
                return
            # Si elige no, dejarle elegir ficha a mover del tablero
            if len(fichas_movibles) > 1:
                self.btnLanzarDado.setEnabled(False)
                self.mostrar_mensaje("Selecciona la ficha que deseas mover haciendo click en la casilla.")
                self._esperando_seleccion = True
                self._valor_dado_pendiente = resultado
                self._conectar_clicks_fichas(fichas_movibles)
            elif len(fichas_movibles) == 1:
                self.presenter.move_ficha_directa(fichas_movibles[0], resultado)
                self.presenter.actualizar_tablero()
            else:
                self.mostrar_mensaje("No hay fichas movibles en el tablero.")
            return
        # Si el dado es 5 y hay fichas en base pero NO hay fichas movibles en el tablero, sacar automáticamente
        if resultado == 5 and fichas_en_base and not fichas_movibles:
            self.presenter.move_active_pion(resultado)
            self.presenter.actualizar_tablero()
            return
        # Si hay más de una ficha movible, esperar selección por click
        if len(fichas_movibles) > 1:
            self.btnLanzarDado.setEnabled(False)
            self.mostrar_mensaje("Selecciona la ficha que deseas mover haciendo click en la casilla.")
            self._esperando_seleccion = True
            self._valor_dado_pendiente = resultado
            self._conectar_clicks_fichas(fichas_movibles)
        else:
            self.presenter.move_active_pion(resultado)
            self.presenter.actualizar_tablero()

    def _conectar_clicks_fichas(self, fichas_movibles):
        self._disconnectors = []
        for ficha in fichas_movibles:
            if ficha.zona == 'tablero':
                index = ficha.posicion + 1
                boton = self.findChild(QPushButton, f"casilla{index}")
                if boton:
                    handler = lambda _, f=ficha: self._on_ficha_click(f)
                    boton.clicked.connect(handler)
                    self._disconnectors.append((boton, handler))
            elif ficha.zona == 'pasillo':
                boton = self.findChild(QPushButton, f"final{ficha.jugador.color.capitalize()}{ficha.posicion}")
                if boton:
                    handler = lambda _, f=ficha: self._on_ficha_click(f)
                    boton.clicked.connect(handler)
                    self._disconnectors.append((boton, handler))

    def _on_ficha_click(self, ficha):
        if not getattr(self, '_esperando_seleccion', False):
            return
        valor = getattr(self, '_valor_dado_pendiente', None)
        if valor is None:
            return
        self.presenter.move_ficha_directa(ficha, valor)
        self.presenter.actualizar_tablero()
        self._desconectar_clicks_fichas()
        self.btnLanzarDado.setEnabled(True)
        self._esperando_seleccion = False
        self._valor_dado_pendiente = None

    def _desconectar_clicks_fichas(self):
        for boton, handler in getattr(self, '_disconnectors', []):
            try:
                boton.clicked.disconnect(handler)
            except Exception:
                pass
        self._disconnectors = []

    def inicializar_fichas(self):
        """
        Muestra todas las fichas al principio.
        """
        fichas = self.presenter.get_fichas()  # recupera la lista de fichas
        for ficha in fichas:
            label = QLabel(self.plateau)  # Widget Añadir al tablero
            label.setText("●")  # O una imagen
            label.resize(20, 20)
            self.labels_fichas.append((ficha, label))
        self.actualizar_fichas()

    def actualizar_fichas(self):
        """
        Actualiza visualmente la posición de las fichas en el tablero.
        """
        for ficha, label in self.labels_fichas:
            pos_logique = ficha.position  # o la propiedad que indica la posición en el tablero
            x, y = self.position_to_coords(pos_logique)  # convierte la posición lógica en coordenadas en la interfaz
            label.move(x, y)
            label.show()
        self.mostrar_fichas_en_base()

    def mostrar_fichas_en_base(self):
        # Limpia primero las fichas dibujadas en las bases
        for color in ["rojo", "azul", "amarillo", "verde"]:
            for i in range(1, 5):
                base_label = self.findChild(QLabel, f"base_{color}_{i}")
                if base_label:
                    base_label.clear()
        # Dibuja solo las fichas que están realmente en base
        jugadores = self.presenter.juego.jugadores
        for jugador in jugadores:
            color = jugador.color.lower()
            fichas_en_base = [f for f in jugador.fichas if f.posicion == -1]
            for idx, ficha in enumerate(fichas_en_base):
                if idx < 4:
                    base_label = self.findChild(QLabel, f"base_{color}_{idx+1}")
                    if base_label:
                        pixmap = QPixmap(f"ficheros_ui/imagenes/pion_{color}.png")
                        base_label.setPixmap(pixmap.scaled(30, 30))
                        base_label.setVisible(True)

    """def position_to_coords(self, pos):
        # Suponga que su tablero tiene una cuadrícula de 10x10, cada cuadrado es de 40x40 píxeles.
        case_taille = 40
        ligne = pos // 10
        colonne = pos % 10
        x = colonne * case_taille
        y = ligne * case_taille
        return x, y"""

    def conectar_senales(self, presenter):
        self.presenter = presenter

    """def abrir_numero_jugadores(self):
        self.ventana_jugadores = VentanaJugadores(self.presenter)
        self.close()
        self.ventana_jugadores.show()"""

    def cerrar(self):
        self.close()
        exit()

    """def mostrar_tablero(self, tablero: Tablero):
        self.mostrar_mensaje("\nTablero:")
        for i, casilla in enumerate(tablero.casillas):
            if casilla.fichas:
                fichas_info = ', '.join(f"Ficha {f.id} ({f.jugador.nombre})" for f in casilla.fichas)
                self.mostrar_mensaje(f"Casilla {i}: {fichas_info}")"""

    """def mostrar_dado(self, resultado: int):
        self.ui.dado.setText(f"{resultado}")"""

    """def actualizar_tablero(self):
        total_casillas = 68
        # Limpiar primero todas las casillas
        for i in range(1, total_casillas + 1):
            self.limpiar_casilla(i)

        # Visualizar las fichas
        for jugador in self.juego.jugadores:
            for ficha in jugador.fichas:
                if ficha.posicion >= 0:
                    index = ficha.posicion + 1  # porque casilla1 corresponde a la posición 0
                    nombre_casilla = f"casilla{index}"
                    boton = self.vista_tablero.findChild(QPushButton, nombre_casilla)

                    if boton:
                        color = ficha.color
                        pixmap = QPixmap(f"ficheros_ui/imagenes/pion_{color}.png")
                        icon = QIcon(pixmap)
                        boton.setIcon(icon)
                        boton.setIconSize(QSize(30, 30))
                    else:
                        print(f"Boton '{nombre_casilla}' irrastreable")"""

    """def leer_input_jugador(self):
        texto = self.lineedit_pieza = QtWidgets.QLineEdit(...)
        if texto.isdigit():
            ficha_id = int(texto)
            self.presenter.mover_ficha_actual(ficha_id)
            self.ui.inputJugador.clear()
        else:
            self.mostrar_mensaje("Por favor, introduce un número válido (0-3).")"""

    """def lanzar_dado(self):
        resultado = self.presenter.lanzar_dado()
        self.mostrar_dado(resultado)
        self.mostrar_mensaje(f"Tira el dado: {resultado}")"""


# --- Clase para la ventana de selección del número de jugadores ---
class VentanaJugadores(VistaBase):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        loadUi("ficheros_ui/numero_jugadores.ui", self)
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
        loadUi("ficheros_ui/PrimeraVentana.ui", self)


class DialogDatosJugador(QDialog):
    """
    Clase DialogDatosJugador:
        Esta clase representa un cuadro de diálogo que permite al usuario introducir
        su nombre y seleccionar un color disponible para su ficha en el juego.
        Se utiliza al configurar los jugadores al inicio de la partida.

        - Muestra un campo de texto para el nombre del jugador.
        - Muestra un menú desplegable con los colores disponibles.
        - Tiene botones para validar (aceptar) o cancelar.
        - El método get_datos() devuelve el nombre y el color seleccionados.
    """

    def __init__(self, colores_disponibles):
        super().__init__()
        self.ui = Ui_DialogJugador()
        self.ui.setupUi(self)
        self.ui.comboBoxCouleur.addItems(colores_disponibles)

        self.ui.btnValider.clicked.connect(self.accept)
        self.ui.btnAnnuler.clicked.connect(self.reject)

    def get_datos(self):
        return self.ui.lineEditNom.text(), self.ui.comboBoxCouleur.currentText()
