from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from LesAventuriersDuRail_gui import *

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Les Aventuriers du Rail")
        self.setGeometry(100, 100, 1000, 700)

        self.joueurs = [Joueur("Alice", "red"), Joueur("Bob", "blue")]
        self.table = Table(self.joueurs, self)
        self.table.initialiser_partie()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label_plateau = QLabel()
        pixmap = QPixmap("plateau.png")
        self.label_plateau.setPixmap(pixmap.scaledToWidth(900, Qt.SmoothTransformation))

        self.bouton_tour = QPushButton("Jouer le prochain tour")
        self.bouton_tour.clicked.connect(self.jouer_tour)

        layout = QVBoxLayout()
        layout.addWidget(self.label_plateau)
        layout.addWidget(self.bouton_tour)

        self.central_widget.setLayout(layout)

    def jouer_tour(self):
        joueur = self.joueurs[0]  # Joueur actif (à améliorer plus tard)
        self.table.jouer_tour(joueur)
        QMessageBox.information(self, "Tour joué", f"{joueur.nom} a joué son tour.")

