from Tablero import Tablero
from Dado import Dado

from PyQt5.QtWidgets import QMainWindow
from ui_parchis_para_pc import Ui_MainWindow

class VistaJuego(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.presenter = presenter

    def conectar_senales(self, presenter):
        self.presenter = presenter
        #self.ui.btnJugar.clicked.connect(self.presenter.iniciar)
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
        print("\nTablero:")
        for i, casilla in enumerate(tablero.casillas):
            if casilla.fichas:
                fichas_info = ', '.join(f"Ficha {f.id} ({f.jugador.nombre})" for f in casilla.fichas)
                print(f"Casilla {i}: {fichas_info}")

    def mostrar_dado(self, resultado: int):
        print(f"Dado: {resultado}")

    def mostrar_mensaje(self, mensaje: str):
        print(mensaje)

    def actualizar_tablero(self):
        pass  # Podría implementarse en interfaz gráfica


from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer


class VentanaJugadores(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        loadUi("numero_jugadores.ui", self)
        self.btn2.clicked.connect(self.elegir_2_jugadores)
        self.btn3.clicked.connect(self.elegir_3_jugadores)
        self.btn4.clicked.connect(self.elegir_4_jugadores)


    def elegir_2_jugadores(self):
        print("2 jugadores elegidos")
        self.close()
        QTimer.singleShot(0, lambda: self.presenter.configurar_jugadores(2))
        # retrasa la ejecución de self.presenter.configurar_jugadores(1) hasta que la ventana actual
        # haya terminado de cerrarse

    def elegir_3_jugadores(self):
        print("3 jugadores elegidos")
        self.close()
        QTimer.singleShot(0, lambda: self.presenter.configurar_jugadores(3))

    def elegir_4_jugadores(self):
        print("4 jugadores elegidos")
        self.close()
        QTimer.singleShot(0, lambda: self.presenter.configurar_jugadores(4))
        
class PrimeraVentana(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        loadUi("PrimeraVentana.ui", self)