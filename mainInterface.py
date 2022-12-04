import sys
from interface import *
from PyQt5.QtWidgets import QMainWindow, QApplication


class InterfaceEstacao(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    iuEstacao = InterfaceEstacao()
    iuEstacao.show()
    qt.exec_()
