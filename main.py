import sys
from PyQt5.QtWidgets import QApplication
from gui import FenetrePrincipale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec_())
