from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogJugador(object):
    def setupUi(self, DialogJugador):
        DialogJugador.setObjectName("DialogJugador")
        DialogJugador.resize(300, 180)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogJugador)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelNom = QtWidgets.QLabel(DialogJugador)
        self.labelNom.setObjectName("labelNom")
        self.verticalLayout.addWidget(self.labelNom)
        self.lineEditNom = QtWidgets.QLineEdit(DialogJugador)
        self.lineEditNom.setObjectName("lineEditNom")
        self.verticalLayout.addWidget(self.lineEditNom)
        self.labelCouleur = QtWidgets.QLabel(DialogJugador)
        self.labelCouleur.setObjectName("labelCouleur")
        self.verticalLayout.addWidget(self.labelCouleur)
        self.comboBoxCouleur = QtWidgets.QComboBox(DialogJugador)
        self.comboBoxCouleur.setObjectName("comboBoxCouleur")
        self.verticalLayout.addWidget(self.comboBoxCouleur)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.btnValider = QtWidgets.QPushButton(DialogJugador)
        self.btnValider.setObjectName("btnValider")
        self.hboxlayout.addWidget(self.btnValider)
        self.btnAnnuler = QtWidgets.QPushButton(DialogJugador)
        self.btnAnnuler.setObjectName("btnAnnuler")
        self.hboxlayout.addWidget(self.btnAnnuler)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(DialogJugador)
        QtCore.QMetaObject.connectSlotsByName(DialogJugador)

    def retranslateUi(self, DialogJugador):
        _translate = QtCore.QCoreApplication.translate
        DialogJugador.setWindowTitle(_translate("DialogJugador", "Ajouter un Joueur"))
        self.labelNom.setText(_translate("DialogJugador", "Nom du joueur :"))
        self.labelCouleur.setText(_translate("DialogJugador", "Choisir une couleur :"))
        self.btnValider.setText(_translate("DialogJugador", "Valider"))
        self.btnAnnuler.setText(_translate("DialogJugador", "Annuler"))
