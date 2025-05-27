import sys
from PyQt5.QtWidgets import QApplication
from VistaJuego import VistaJuego, PrimeraVentana
from Juego import Juego
from JuegoPresenter import JuegoPresenter
from PyQt5.QtCore import Qt, QTimer

def ciclo_de_juego():
    app = QApplication(sys.argv)
    juego = Juego()

    vista = VistaJuego(None)
    presenter = JuegoPresenter(vista, juego)
    vista.presenter = presenter
    vista.conectar_senales(presenter)

    ventana = PrimeraVentana(presenter)
    ventana.show()


    QTimer.singleShot(3000, lambda: (
        ventana.close(),
        vista.show()
    ))

    app.exec_()

    while True:
        jugador = juego.jugadores[juego.turno_actual]
        vista.mostrar_mensaje(f"\nTurno de {jugador.nombre}")
        input("Presiona Enter para lanzar el dado...")
        resultado = presenter.lanzar_dado()

        ficha_id = int(input(f"Selecciona la ficha (0-3) para mover {resultado} pasos: "))
        if presenter.mover_ficha(jugador, ficha_id, resultado):
            break


if __name__ == "__main__":
    ciclo_de_juego()