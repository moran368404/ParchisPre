from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from Dado import Dado

class DialogTiradaInicial(QDialog):
    def __init__(self, jugadores, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tirada inicial de dados")
        self.jugadores = jugadores
        self.resultados = {j: None for j in jugadores}
        self.dado = Dado(6)
        self.layout = QVBoxLayout()
        self.labels = {}
        self.botones = {}
        self.setLayout(self.layout)
        self.info_label = QLabel("Cada jugador tira el dado. El más alto comienza.")
        self.layout.addWidget(self.info_label)
        for jugador in jugadores:
            label = QLabel(f"{jugador.nombre}: ?")
            self.labels[jugador] = label
            btn = QPushButton(f"Tirar dado {jugador.nombre}")
            btn.clicked.connect(lambda checked, j=jugador: self.tirar_dado(j))
            self.botones[jugador] = btn
            self.layout.addWidget(label)
            self.layout.addWidget(btn)
        self.btn_finalizar = QPushButton("Finalizar selección")
        self.btn_finalizar.setEnabled(False)
        self.btn_finalizar.clicked.connect(self.finalizar)
        self.layout.addWidget(self.btn_finalizar)

    def tirar_dado(self, jugador):
        if self.resultados[jugador] is not None:
            QMessageBox.information(self, "Ya tiró", f"{jugador.nombre} ya tiró el dado.")
            return
        valor = self.dado.lanzar()
        self.resultados[jugador] = valor
        self.labels[jugador].setText(f"{jugador.nombre}: {valor}")
        self.botones[jugador].setEnabled(False)
        if all(v is not None for v in self.resultados.values()):
            self.btn_finalizar.setEnabled(True)

    def finalizar(self):
        max_val = max(self.resultados.values())
        ganadores = [j for j, v in self.resultados.items() if v == max_val]
        if len(ganadores) == 1:
            self.ganador = ganadores[0]
            self.accept()
        else:
            # Empate: solo los empatados vuelven a tirar
            QMessageBox.information(self, "Empate", "Empate entre: " + ", ".join(j.nombre for j in ganadores) + ". Solo ellos vuelven a tirar.")
            for j in self.jugadores:
                if j in ganadores:
                    self.resultados[j] = None
                    self.labels[j].setText(f"{j.nombre}: ?")
                    self.botones[j].setEnabled(True)
                else:
                    self.botones[j].setEnabled(False)
            self.btn_finalizar.setEnabled(False)

    def get_ganador(self):
        return getattr(self, 'ganador', None)
