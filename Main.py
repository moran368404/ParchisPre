import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from Juego import Juego
from JuegoPresenter import JuegoPresenter
from VistaJuego import VistaParchis, VistaTablero, PrimeraVentana, VentanaJugadores


def main():
    app = QApplication(sys.argv)
    juego = Juego()

    # Instanciar vistas
    ventana_inicio = PrimeraVentana(None)
    vista_parchis = VistaParchis(None)
    ventana_jugadores = VentanaJugadores(None)
    vista_tablero = VistaTablero()

    # Crear presentador y vincular vistas
    presenter = JuegoPresenter(vista_parchis, juego)
    presenter.vista_inicio = ventana_inicio
    presenter.vista_parchis = vista_parchis
    presenter.vista_jugadores = ventana_jugadores
    presenter.vista_tablero = vista_tablero

    ventana_inicio.presenter = presenter
    vista_parchis.presenter = presenter
    ventana_jugadores.presenter = presenter
    vista_tablero.set_presenter(presenter)

    vista_parchis.conectar_senales(presenter)
    vista_tablero.conectar_senales(presenter)

    ventana_inicio.show()

    # Cambio automático a vista_parchis después de 3so
    def mostrar_menu_parchis():
        ventana_inicio.close()
        vista_parchis.show()

    QTimer.singleShot(3000, mostrar_menu_parchis)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
